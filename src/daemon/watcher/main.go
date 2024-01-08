package main

import (
    "database/sql"
    "os"
    "fmt"
    "log"
    "time"
    "github.com/streadway/amqp"

    _ "github.com/lib/pq"
)

const (
    CONNECTION_STR_XML = "user=is password=is dbname=is host=db-xml sslmode=disable"
)

type ImportedDocument struct {
    Id          int
    Filename    string
    Created_on  string
    Updated_on  string
    Deleted_on  string
    Is_migrated bool
}

type Task struct {
    Type   string
    Entity ImportedDocument
    Body   string
}

func sendDocumentShouldMigrateMessage(documentId string, queue amqp.Queue, channel *amqp.Channel) {
    err := channel.Publish(
        "",
        queue.Name,
        false,
        false,
        amqp.Publishing{
            ContentType: "text/plain",
            Body:        []byte(documentId),
            Priority:    0,
        },
    )

    if err != nil {
        log.Fatalf("Failed to publish a message: %s", err)
    }

    fmt.Println("Queue: ", queue)
    fmt.Println("Published Successfully")
}

func ImportedDocuments() []ImportedDocument {
    var imported_documents []ImportedDocument

    conn, err := sql.Open("postgres", CONNECTION_STR_XML)
    if err != nil {
        log.Fatalf("Failed to connect to PostgreSQL: %s", err)
    }

    if conn.Ping() != nil {
        panic("Can't ping")
    }

    if conn == nil {
        panic("Connection is nil")
    }

    documents, err := conn.Query("SELECT id, file_name, created_on, updated_on, deleted_on, is_migrated FROM imported_documents;")
    if err != nil {
        log.Fatalf("Failed to query documents: %s", err)
    }

    for documents.Next() {
        var document ImportedDocument

        err := documents.Scan(&document.Id, &document.Filename, &document.Created_on, &document.Updated_on, &document.Deleted_on, &document.Is_migrated)
        if err != nil {
            log.Fatalf("Failed to scan document: %s", err)
        }

        imported_documents = append(imported_documents, document)
    }

    documents.Close()
    conn.Close()
    return imported_documents
}

func (doc *ImportedDocument) Print() {
    fmt.Printf("%d: %s\n", doc.Id, doc.Filename)
}

func GenerateTasks(docs []ImportedDocument) []Task {
    var tasks []Task
    var updateTasks []Task

    maxRetries := 5
    retryDelay := time.Second * 5

    var conn *amqp.Connection
    var err error

    for i := 0; i < maxRetries; i++ {
        connStr := fmt.Sprintf("amqp://%s:%s@broker:5672/%s",
            os.Getenv("RABBITMQ_DEFAULT_USER"),
            os.Getenv("RABBITMQ_DEFAULT_PASS"),
            os.Getenv("RABBITMQ_DEFAULT_VHOST"))
        conn, err = amqp.Dial(connStr)
        if err == nil {
            break
        }

        log.Printf("Failed to connect to RabbitMQ: %s", err)
        log.Printf("Retrying in %v seconds...", retryDelay.Seconds())
        time.Sleep(retryDelay)
    }

    if err != nil {
        log.Fatalf("Failed to connect to RabbitMQ: %s", err)
    }
    defer conn.Close()

    ch, err := conn.Channel()
    if err != nil {
        log.Fatalf("Failed to open a channel: %s", err)
    }
    defer ch.Close()

    // Declare the migrator queue
    migratorQueue, err := ch.QueueDeclare(
        "migrator_queue", // name
        true,             // durable
        false,            // delete when unused
        false,            // exclusive
        false,            // no-wait
        nil,              // arguments
    )
    if err != nil {
        log.Fatalf("Failed to declare the migrator queue: %s", err)
    }

    // Declare the gis-updater queue
    gisUpdaterQueue, err := ch.QueueDeclare(
        "gis_updater_queue", // name
        true,                // durable
        false,               // delete when unused
        false,               // exclusive
        false,               // no-wait
        nil,                 // arguments
    )
    if err != nil {
        log.Fatalf("Failed to declare the gis-updater queue: %s", err)
    }

    for _, doc := range docs {
        var queueName string
        var body string

        if doc.Is_migrated {
            queueName = gisUpdaterQueue.Name
            body = "Activate"
        } else {
            queueName = migratorQueue.Name
            body = fmt.Sprintf("File ID: %d", doc.Id)
        }

        log.Printf("Sending message: %s to queue: %s", body, queueName)

        task := Task{
            Type:   queueName,
            Entity: doc,
            Body:   body,
        }

        if doc.Is_migrated {
            tasks = append(tasks, task)
            body = "Activate"
            log.Printf("doc.Is_migrated is true for doc.Id: %d", doc.Id)
        } else {
            updateTasks = append(updateTasks, task)
        }
    }

    // Publish migration tasks
    for _, task := range tasks {
        err = ch.Publish(
            "",        // exchange
            task.Type, // routing key
            false,     // mandatory
            false,     // immediate
            amqp.Publishing{
                ContentType: "text/plain",
                Body:        []byte(task.Body),
            })
        if err != nil {
            log.Fatalf("Failed to publish a message: %s", err)
        }
    }

    // Publish update tasks
    for _, task := range updateTasks {
        err = ch.Publish(
            "",        // exchange
            task.Type, // routing key
            false,     // mandatory
            false,     // immediate
            amqp.Publishing{
                ContentType: "text/plain",
                Body:        []byte(task.Body),
            })
        if err != nil {
            log.Fatalf("Failed to publish a message: %s", err)
        }
    }

    return append(tasks, updateTasks...)
}

func ProcessTasks(tasks []Task) {
    for _, task := range tasks {
        switch task.Type {
        case "migrator_queue":
            fmt.Println("Migrating document:", task.Entity.Filename)
        case "gis_updater_queue":
            if task.Entity.Is_migrated {
                fmt.Println("Updating geographic data:", task.Entity.Filename)
            } else {
                fmt.Println("Skipping geographic data update task for not migrated document:", task.Entity.Filename)
            }
        }
    }
}

func main() {
    sentIds := make(map[int]bool) // Keep track of sent IDs
    migratedStatus := make(map[int]bool) // Keep track of migrated status

    for {
        docs := ImportedDocuments()

        // Filter out documents that have already been sent
        var newDocs []ImportedDocument
        for _, doc := range docs {
            // If the document hasn't been sent yet, or its migrated status has changed
            if !sentIds[doc.Id] || doc.Is_migrated != migratedStatus[doc.Id] {
                newDocs = append(newDocs, doc)
                sentIds[doc.Id] = true // Mark this ID as sent
                migratedStatus[doc.Id] = doc.Is_migrated // Update the migrated status
            }
        }

        // Generate and process tasks for new documents
        if len(newDocs) > 0 {
            tasks := GenerateTasks(newDocs)
            ProcessTasks(tasks)
        }

        // Sleep for a while before checking again
        time.Sleep(time.Second * 30)
    }
}

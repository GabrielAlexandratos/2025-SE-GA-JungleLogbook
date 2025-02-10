# Design

At every stage of development we can and should review decisions made in previous stages to ensure that they are still valid and beneficial. Doing this early can save a lot of time and effort later on when changes are required or the solution does not meet the requirements.


## User Activity Diagram
``` mermaid

flowchart TD
    %% Actors
    User(("User"))
    Admin(("Admin"))

    %% Use Cases
    Login["Login"]
    Register["Register"]
    AddExpense["Add Expense"]
    ViewExpenses["View Expenses"]
    EditExpense["Edit Expense"]
    DeleteExpense["Delete Expense"]

    %% Actor Relationships
    User --> Login
    User --> Register
    User --> AddExpense
    User --> ViewExpenses
    User --> EditExpense
    User --> DeleteExpense
    Admin --> Login

    %% Use Case Dependencies
    Register -->|"enables"| Login
    Login -->|"required for"| AddExpense
    Login -->|"required for"| ViewExpenses
    Login -->|"required for"| EditExpense
    Login -->|"required for"| DeleteExpense
    AddExpense -->|"updates"| ViewExpenses
    ViewExpenses -->|"select for"| EditExpense
    ViewExpenses -->|"select for"| DeleteExpense

    %% Notes
    subgraph Preconditions
        note1["All actions except Register
        require user authentication"]
    end

```

This Mermaid diagram provides a visual representation of the user activity flow in your application. It includes actors (User and Admin), use cases (Login, Register, Add Expense, View Expenses, Edit Expense, Delete Expense), and relationships between them. The diagram also shows dependencies between use cases and notes on preconditions for certain actions.

## Class Diagram
```mermaid
classDiagram
    class User {
        +username: string
        +password: string
        +email: string
        +expenses: Array<Expense>
    }

    class Admin {
        +username: string
        +password: string
        +role: "Admin"
    }

    class ExpenseTracker {
        +users: Array<User>
        +admin: Admin
    }

    class Login {
        -username: string
        -password: string
        +result: boolean
    }

    class Register {
        -email: string
        -password: string
        +result: boolean
    }

    class AddExpense {
        -date: date
        -description: string
        -amount: number
        -category: string
    }

    class ViewExpenses {
        -dateRange: dateRange
        -category: string
    }

    class EditExpense {
        -expenseId: number
        -newDate: date
        -newDescription: string
        -newAmount: number
        -newCategory: string
    }

    class DeleteExpense {
        -expenseId: number
    }

    User "1" --* ExpenseTracker : has account
    Admin "1" --* ExpenseTracker : manages configuration

    Login ..> AddExpense : after login, user can add new expenses
    Register ..> Login : registered user can log in
    AddExpense ..> ViewExpenses : after adding expense, user can view updated expenses
    ViewExpenses ..> EditExpense : from list of expenses, user can edit or delete individual expenses

    ExpenseTracker *-- User : tracks user's expenses
```

This diagram shows the relationships between different classes and their interactions within an expense tracking system. It includes classes for login, registration, adding expenses, viewing expenses, editing expenses, and deleting expenses. The `ExpenseTracker` class is central to managing these operations for a user or admin.

## Sequence Diagrams
Sequence diagrams are used to show the flow of messages between objects over time. They help in understanding how different components interact with each other in a specific scenario. Below is an example of creating a new expense in the expense tracking system.

```mermaid
sequenceDiagram
    participant User as "User"
    participant System as "System"

    Note over User:System running and user has valid account

    User->>System: Login with username/password
    System->>User: Authenticate user and grant access to expense tracker

    Note over User:UI displays add expense form

    User->>System: Add new expense with details (date, description, amount, category)
    System->>User: Create new expense entry in database

    Note over User:UI displays updated list of expenses

    User->>System: View own expenses
    System->>User: Display list of expenses with filters and sorting options
```

[< Prev: Requirements](./requirements_and_analysis.md) | [Next: Implementation >](./implementation.md)
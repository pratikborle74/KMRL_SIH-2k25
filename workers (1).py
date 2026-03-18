import csv
import json


# Function to load the workers from the CSV file
def load_workers_from_csv(csv_filename):
    workers = []
    with open(csv_filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        fieldnames = csv_reader.fieldnames  # Get the column headers from the CSV
        print(f"CSV columns: {fieldnames}")  # Debugging line to check column names

        # Check if the required column 'Availability' exists
        if 'Availability' not in fieldnames:
            print("Warning: 'Availability' column is missing. Adding it with default 'Yes' value.")
            workers = [{**row, 'Availability': 'Yes'} for row in csv_reader]  # Add 'Availability' dynamically
        else:
            workers = list(csv_reader)  # Convert rows into a list of dictionaries
    return workers


# Function to save workers' updated data back to CSV
def save_workers_to_csv(csv_filename, workers):
    with open(csv_filename, mode='w', newline='') as file:
        fieldnames = ['Worker ID', 'Name', 'Age', 'Gender', 'Station Assigned', 'Shift Timing', 
                      'Duties', 'Supervisor', 'Contact Number', 'Employment Status', 
                      'Induction Status', 'Inspection Slot', 'Inspection Outcome', 
                      'Availability', 'Task', 'Task Time (mins)']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(workers)


# Convert workers list to JSON format
def workers_to_json(workers):
    return json.dumps(workers, indent=4)


# Function to assign task to a worker
def assign_task_to_worker(workers, worker_id, task, task_time):
    for worker in workers:
        if worker['Worker ID'] == str(worker_id) and worker.get('Availability', 'No') == 'Yes':
            worker['Task'] = task
            worker['Task Time (mins)'] = task_time
            worker['Availability'] = 'No'  # Worker is now assigned to a task
            return worker
    return None


# Function to mark a worker as available again after task completion
def complete_task(workers, worker_id):
    for worker in workers:
        if worker['Worker ID'] == str(worker_id) and worker.get('Availability', 'No') == 'No':
            # Worker has a task assigned, now mark as available and clear task details
            worker['Task'] = ''
            worker['Task Time (mins)'] = 0
            worker['Availability'] = 'Yes'  # Worker is now available again
            
            # Display a message that task has been completed
            print(f"Task for {worker['Name']} has been completed. Worker is now available.")
            
            return worker
    return None


# Main function
def main():
    csv_filename = 'workers.csv'  # Path to the CSV file
    workers = load_workers_from_csv(csv_filename)
   
    while True:
        print("\nSelect an option:")
        print("1. View All Workers (JSON Output)")
        print("2. Assign Task to Worker")
        print("3. Complete Task")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            # View all workers in JSON format
            workers_json = workers_to_json(workers)
            print(workers_json)

        elif choice == '2':
            # Assign task to a worker
            worker_id = input("Enter Worker ID to assign task: ").strip()
            task = input("Enter Task Name (e.g., Dry Waste, Wet Waste): ").strip()
            task_time = input("Enter Task Time (in minutes): ").strip()
            updated_worker = assign_task_to_worker(workers, worker_id, task, task_time)

            if updated_worker:
                print(f"Task '{task}' has been assigned to {updated_worker['Name']} for {task_time} minutes.")
                save_workers_to_csv(csv_filename, workers)
            else:
                print(f"Worker with ID {worker_id} is not available or doesn't exist.")

        elif choice == '3':
            # Complete task and mark worker as available again
            worker_id = input("Enter Worker ID to complete task: ").strip()
            updated_worker = complete_task(workers, worker_id)

            if updated_worker:
                # The task completion message will be printed in complete_task() function
                save_workers_to_csv(csv_filename, workers)
            else:
                print(f"Worker with ID {worker_id} does not have any assigned task or doesn't exist.")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()

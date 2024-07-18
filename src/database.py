from nurse import *

def save_workers_to_json(workers, filename):
    data = {
        'workers': [worker.to_dict() for worker in workers]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_workers_from_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            workers = []
            for worker_data in data['workers']:
                workers.append(Nurse.from_dict(worker_data))
            return workers
    except FileNotFoundError:
        print(f"No caretakers found - file {filename} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON data in file {filename}")
        return []
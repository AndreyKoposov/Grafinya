async function api_process_create(name) {
    await fetch("api/processes/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: name }),
    })
    .catch(error => console.error(error));
}

async function api_process_rename(id, new_name) {
    await fetch("api/processes/rename", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ pr_id: id, new_name: new_name }),
    })
    .catch(error => console.error(error));
}

async function api_process_delete(id) {
    await fetch("api/processes/delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ pr_id: id }),
    })
    .catch(error => console.error(error));
}

async function api_processes_get() {
    processes = []

    await fetch("api/processes/")
        .then(response => response.json())  
        .then(data => processes = data.processes)
        .catch(error => console.error(error));

    return processes
}

async function api_fetch_msgs() {
    msgs = []

    await fetch("api/messages/")
        .then(response => response.json())  
        .then(data => msgs = data.msgs)
        .catch(error => console.error(error));

    return msgs
}

async function api_check_msgs() {
    has_new = false;

    await fetch("api/messages/check")
        .then(response => response.json())  
        .then(data => has_new = data.has_new)
        .catch(error => console.error(error));

    return has_new
}

async function api_send_msg(text) {
    await fetch("api/messages/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
    })
    .catch(error => console.error(error));
}
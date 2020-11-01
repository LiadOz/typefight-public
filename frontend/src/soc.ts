import io from 'socket.io-client'

const endpoint = 'http://127.0.0.1:5000';

const entry = io(endpoint);
entry.on('login', (player_id: number) => {
    const url = endpoint + "/data" + player_id;
    console.log("logging with player " + player_id);
    console.log(url);
    const socket = io(url);
    socket.on('start', log_data);
    socket.on('change', log_data);

    socket.on('connect', () => {
        entry.emit('logged_in', {'id': player_id});
    });
});
entry.emit('login');

function log_data(data: string): void {
    console.log(data);
};

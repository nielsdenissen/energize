const URL = "ws://4bf6a8c8.ngrok.io/media";

export const socket = new WebSocket(URL);

socket.onopen = () => {
  console.log("sockets connection opened");
};

socket.onclose = () => {
  console.log("socket connection closed");
};

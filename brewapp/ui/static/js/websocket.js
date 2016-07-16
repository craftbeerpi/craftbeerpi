function mySocket (socketFactory) {
  var myIoSocket = io.connect('/brew');

  mySocket = socketFactory({
    ioSocket: myIoSocket
  });
  mySocket.forward('config');
  mySocket.forward('temp_udpdate');
  mySocket.forward('kettle_update');
  mySocket.forward('kettle_state_update');
  mySocket.forward('switch_state_update');
  mySocket.forward('timer_update');
  mySocket.forward('step_update');
  mySocket.forward('message');




  return mySocket;
}


angular.module("cbpwebsocket", [])
.factory("mySocket", mySocket);

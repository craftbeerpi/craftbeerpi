function mySocket (socketFactory) {

  var url = 'http://' + document.domain + ':' + location.port + '/brew' ;
  var myIoSocket = io.connect(url);

  mySocket = socketFactory({
    ioSocket: myIoSocket
  });

  //mySocket.emit("coonect");
  mySocket.forward('config');
  mySocket.forward('temp_udpdate');
  mySocket.forward('kettle_update');
  mySocket.forward('kettle_state_update');
  mySocket.forward('switch_state_update');
  mySocket.forward('timer_update');
  mySocket.forward('step_update');
  mySocket.forward('message');
  mySocket.forward('fermenter_update');



  return mySocket;
}


angular.module("cbpwebsocket", [])
.factory("mySocket", mySocket);

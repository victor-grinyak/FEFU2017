<template>
  <div id="app">
  	<div id = 'my-map' style="width: 100%; height: 100%"></div>
  	<my-header @createLoginWindow = 'showModal = true' @createRegWindow = 'showReg = true'></my-header>

    <modal v-if = 'showModal' @openRegWindow = 'showReg = true' @close = 'showModal = false' ></modal>

    <modal-reg v-if = 'showReg' @closeReg = 'showReg = false'></modal-reg>

     
      <div class="col-md-3 col-lg-3 col-sm-3">
    	   <todo-list @todosCollected = 'makeMarkers'  :myMap='myMap'></todo-list>
      </div>
  			
  </div>
</template>



<script>
  import 'bootstrap/dist/css/bootstrap.css';
  import Modal from './components/modal-login.vue';
  import ModalReg from './components/modal-reg.vue';
  import { yandexMap, ymapMarker } from 'vue-yandex-maps'

export default {
	methods:{
    makeMarkers(obj){
      //alert(obj)
      this.todoItems = obj;
    }
  },
    data(){
    return{
       mapHeight: "",
       loginWindow: false,
       showModal: false,
       showReg: false,
       myMap: {}
    }
  },
  created(){
    this.mapHeight = document.body.clientHeight + "px";
    var self = this;
    ymaps.ready(function(){
      self.myMap = new ymaps.Map("my-map", {
            center: [43.115141, 131.885341], 
            zoom: 12,
            behaviors: ['drag', 'scrollZoom', 'multiTouch'],
            controls: []
        });
      var zoomControl = new ymaps.control.ZoomControl({
          options: {
              size: "auto",
              position:{
                  right: 5,
                  top: 75
              }
          }
      });
      var geoControl = new ymaps.control.GeolocationControl({
          options: {
              float: 'right'
          }
      });
      self.myMap.controls.add(zoomControl);
      //self.myMap.controls.add(geoControl);
    });
  },
  components:{
    'modal':Modal,
    'modal-reg': ModalReg,
    yandexMap,
    ymapMarker
  }
}
</script>


<style>
#todo-list{
  padding: 0px;
  
}
#loll{
  margin-bottom: -10px;
}
.row{
  margin-left: 0px;
}
#login{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.ymap-container{
  width: 100%;
  
  padding: 0px;
  position: absolute;
}
#my-map{
  width: 100%;

  padding: 0px;
  position: absolute;
}
</style>

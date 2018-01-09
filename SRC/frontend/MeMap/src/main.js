import Vue from 'vue';
import App from './App.vue';
import TodoList from './components/Todo-list.vue';
import Head from './components/Head-component.vue';
import VueScrollTo from 'vue-scrollto';

Vue.use(VueScrollTo);
Vue.component('todo-list', TodoList);
Vue.component('my-header', Head)

new Vue({
  el: '#app',
  render: h => h(App),
  methods: {
  	// 		init(){
			// 	myMap = new ymaps.Map("my-map", {
   //          	center: [55.76, 37.64],
   //         		zoom: 7
   //      		});
			// }
  }
});

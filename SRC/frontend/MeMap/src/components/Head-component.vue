<template>
	<div id = 'my-header'>
     	 <nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">MeMap</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      
      <ul class="nav navbar-nav navbar-right">
         <li v-if = 'login'><a>{{login}}</a></li>
         <li v-if = 'login'><a href="#" @click = 'logout'>Выход</a></li>

         <li v-if = '!login'><a href="#" @click = '$emit("createLoginWindow")'>Вход</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
	</div>
</template>

<script>
	export default{
    data(){
      return{
        token: '',
        login: ''
      }
    },
    methods:{
      logout(){

        this.login = '';
        alert('logged out');
        localStorage.removeItem('login');
        localStorage.removeItem('token');
        window.location.reload(false);
      }

    },
    created(){
      this.login = localStorage.getItem('login');
    },
    mounted(){

    }
	}
</script>

<style >
.navbar{
  width: 100%;
  margin: 0px;
}

</style>
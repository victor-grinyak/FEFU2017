<template>
	<div id= 'log'>
		<div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            <h3>Вход</h3>
          </div>

          <div class="modal-body">
            <form>
            	<input id ='loginInput' class = 'form-control' type="text" name="login" placeholder="Логин">
            	<input id = 'loginPassword' class = 'form-control' type="password" name="password" placeholder="Пароль">
            </form>
          </div>

          <div class="modal-footer">
          	<a id = 'reg' @click = 'openRegWindow'>Регистрация</a>
          	<button class = 'btn btn-default' @click = '$emit("close")'>Отмена</button>
            <button class = 'btn btn-default' @click = 'submitLogin'>Вход</button>
          </div>
        </div>
      </div>
    </div>
	</div>
</template>

<script>
	export default{
    data(){
      return{
        login:""
      }
    },
		methods:{
			submitLogin(){
        this.login = document.getElementById('loginInput').value
        let self = this;
        $.ajax({
          url: 'https://memap.ddns.net/api/auth?' + $.param({ login: self.login, password:document.getElementById('loginPassword').value }),
          method: 'GET',
          
          success: function(data){
            console.log(data);
            localStorage.setItem('token', data.token);
            localStorage.setItem('login', self.login);
            window.location.reload(false);


          },
          error: function(msg){
            console.log(msg);
          }
        });
				//this.$emit('successfulLogin', token);
			},
			openRegWindow(){
				this.$emit('close');
				this.$emit('openRegWindow')
			}
		}
	}
</script>
<style type="text/css">
	
.modal-mask {

  z-index: 9998;

  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;

  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 30%;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

#reg{
	float: left;
}
</style>
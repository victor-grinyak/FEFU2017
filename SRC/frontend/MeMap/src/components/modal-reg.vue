<template>
	<div id = 'reg'>
		<div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            <h3>Регистрация</h3>
          </div>

          <div class="modal-body">
            <form  method="post" name = 'regForm'>
            	<input id = 'loginReg' class = 'form-control' type="text" name="login" placeholder="Логин">
            	<input id = 'passwordReg' class = 'form-control' type="password" name="password" placeholder="Пароль">
              
            </form>
          </div>

          <div class="modal-footer">
          	<button class = 'btn btn-default' @click = '$emit("closeReg")'>Отмена</button>
            <button class = 'btn btn-default' @click = 'submitReg' >Регистрация</button>
          </div>
        </div>
      </div>
    </div>
	</div>
</template>

<script>
	export default{
		methods:{
			submitReg(){  
        $.ajax({
          url: 'https://memap.ddns.net/api/reg?' + $.param({ login: document.getElementById('loginReg').value, password:document.getElementById('passwordReg').value }),
          method: 'POST',
          
          success: function(data){
            localStorage.setItem('token', data.token);
            localStorage.setItem('login', document.getElementById('loginReg').value);
            window.location.reload(false);
          }
        });
				//this.$emit('successfulLogin', token);
			}
		}
	}
</script>
<style>
	
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


</style>
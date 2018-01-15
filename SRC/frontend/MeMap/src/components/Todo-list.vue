<template>
    <div id='todo-list' @dataCollected='dosmth'>
        <button type="button" id='viewButton' class="btn btn-secondary btn-lg" @click="viewAddMenu"
                :disabled='buttonDisabled'> Добавить заметку
        </button>

        <div id='addDiv' v-if="viewMenu">
            <form id="createForm">
                <input id="createTitle" class="form-control" type="textaria" name="title" v-model='title'
                       placeholder="Название заметки" maxlength="32">

                <date-picker id='datepicker' v-model="date" :config="config" placeholder="Выберите время"></date-picker>

                <input id="comment" class="form-control" type="textaria" name="title" v-model='commentary'
                       placeholder="Описание" maxlength="5000">

                <div class="input-group" style="{margin-bottom: 3px}">
                    <input id='createAdress' class='form-control' type="textaria" name="adress"
                           placeholder="Выберите адрес на карте" style="margin-bottom: 3px" :value='adress'
                           readonly='true'>
                    <span class="input-group-btn">
							        <button class="btn btn-secondary" type="button"
                                            @click='choosePlace'>Выбрать</button>
							    </span>
                </div>
            </form>
        </div>

        <div id='itemList' :style="{height: itemListHeight+'px'}">
            <ul id='list'>
                <li is='todo-item'
                    v-for="item in todoItems"
                    :title='item.header'
                    :pos='[item.lattitude, item.longitude]'
                    :adress='item.location_str'
                    :time='item.date'
                    :description='item.description'
                    :myMap='myMap'
                    :id='item.id'
                    @scrollTo='scrollToItem'
                    @deleteItem='deleteItem'
                    @doneItem='doneItem'
                >
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import datePicker from 'vue-bootstrap-datetimepicker';
    import 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.css';

    import todoItem from './Todo-item.vue';
    //import todoAdd from './Todo-add.vue';


    export default {
        data() {
            return {
                todoItems: [],
                itemListHeight: window.innerHeight - 15 - 52 - 50,
                date: "",
                config: {
                    useCurrent: false,
                    showClear: true,
                    showClose: true,
                    //collapse: false,
                    minDate: new Date(),
                    widgetPositioning: {
                        horizontal: 'right',
                        vertical: 'auto'
                    }
                },
                viewMenu: false,
                title: "",
                location: [],
                adress: "",
                commentary: "",
                token: "",
                buttonDisabled: true,
                callback: {},
                myPlacemark: ''
            }
        },

        props: {
            myMap: Object
        },
        methods: {
            deleteItem(id) {
                let self = this;
                for (let i in this.todoItems)
                    if (this.todoItems[i].id == id) {

                        $.ajax({
                            url: 'https://memap.ddns.net/api/notes/' + id + '?' + $.param({
                                token: self.token,
                            }),
                            method: 'DELETE',
                            success() {
                                console.log('удалено');
                            },
                            error(err) {

                            }
                        });
                        this.todoItems.splice(i, 1);
                        break;
                    }
            },
            doneItem(id) {
                let self = this;
                for (let i in this.todoItems)
                    if (this.todoItems[i].id == id) {
                        var item = this.todoItems[i];
                        $.ajax({
                            url: 'https://memap.ddns.net/api/notes/' + id + '?' + $.param({
                                token: self.token,
                                header: item.header,
                                date: item.date,
                                lattitude: item.lattitude,
                                longitude: item.longitude,
                                description: item.description,
                                is_archived: true
                            }),
                            method: 'PUT',
                            success(item) {
                                self.todoItems.splice(i, 1);
                            },
                            error(err) {
                                console.log('ошибка при выполнении заметки');
                            }
                        });
                        break;
                    }
            },

            choosePlace() {
                let map = document.getElementById('my-map');
                let self = this;
                ymaps.ready(function () {

                    self.callback = function (e) {
                        var coords = e.get('coords');
                        self.location = coords;
                        // Если метка уже создана – просто передвигаем ее.
                        if (self.myPlacemark) {
                            self.myPlacemark.geometry.setCoordinates(coords);
                        }
                        else {
                            self.myPlacemark = new ymaps.Placemark(coords);
                            self.myMap.geoObjects.add(self.myPlacemark);
                            // Слушаем событие окончания перетаскивания на метке.
                        }
                        self.myPlacemark.item = self;
                        //       myPlacemark.events.add('click', function(e){
                        // 	ymaps.geoQuery(self.myMap.geoObjects)
                        // 	.each(function(pm){
                        // 		pm.options.set('preset', 'islands#blueIcon');
                        // 	});
                        // 	self.$emit('scrollTo', self.id)
                        // 	myPlacemark.options.set('preset', 'islands#yellowIcon');
                        // 	self.myMap.panTo(self.pos);
                        // });
                        //myPlacemark.properties.set('iconCaption', 'Поиск...');
                        ymaps.geocode(coords).then(function (res) {
                            var firstGeoObject = res.geoObjects.get(0);
                            self.adress = firstGeoObject.getAddressLine();
                            self.myPlacemark.properties
                                .set({
                                    // Формируем строку с данными об объекте.
                                    iconCaption: firstGeoObject.getAddressLine(),
                                    // В качестве контента балуна задаем строку с адресом объекта.
                                    balloonContent: firstGeoObject.getAddressLine()
                                });
                        });

                    };
                    self.myMap.events.add('click', self.callback);
                });
            },
            scrollToItem(id) {
                //let container = document.getElementById('list');
                let el = document.getElementById('id' + id);

                var cancelScroll = this.$scrollTo(el, 200, {
                    container: '#list',
                    easing: 'ease-in',
                    offset: 0,
                    cancelable: true,
                    onDone: function () {
                        console.log('ok')
                    },
                    onCancel: function () {
                        // scrolling has been interrupted
                    },
                    x: false,
                    y: true
                });
                el.style['border-color'] = 'green';
                //console.log(el);
            },
            dosmth(obj) {
                for (var note in obj.notes)
                    this.todoItems.push(note);
            },
            viewAddMenu() {
                if (this.viewMenu) {
                    let el = document.getElementById('addDiv');
                    let item = {};

                    item.header = document.getElementById('createTitle').value;
                    item.time = new Date(document.getElementById('datepicker').value).getTime();
                    item.description = document.getElementById('comment').value;
                    item.pos = this.location;
                    if (this.validate(item)) {
                        let self = this;
                        $.ajax({
                            url: 'https://memap.ddns.net/api/notes?' + $.param({
                                token: self.token,
                                header: item.header,
                                date: item.time,
                                lattitude: item.pos[0],
                                longitude: item.pos[1],
                                description: item.description,
                                is_archived: false
                            }),
                            method: 'POST',
                            success(data) {
                                if (data.ok == true) {
                                    self.todoItems.push(data.note);
                                }
                                else
                                    console.log('неверная заметка');
                            },
                            error(err) {

                            }
                        });
                    }
//                    document.getElementById('createTitle').value = '';
                    this.viewMenu = !this.viewMenu;
                    this.myMap.events.remove('click', this.callback);
                    this.myMap.geoObjects.remove(this.myPlacemark);
                    location.reload();
                }
                else {
                    this.viewMenu = !this.viewMenu;
                    this.myMap.events.remove('click', this.callback);
                }
            },
            validate(item) {
                if (item.header == '')
                    return false;
                if (item.time == '')
                    return false;
                let date = Date.parse(item.time);
                if (date < Date.now())
                    return false;

                return true;

            }
        },
        created() {
            this.token = localStorage.getItem('token');
            let t = this.token;
            if (this.token) {
                this.buttonDisabled = false;
                $.ajax({
                    url: 'https://memap.ddns.net/api/notes?' + $.param({token: t}),
                    method: 'GET',

                    success: (data) => {
                        for (let note in data.notes)
                            this.todoItems.push(data.notes[note]);
                    },
                    error: function (msg) {
                        console.log(msg);
                    }
                });
            }
        },
        components: {
            'todo-item': todoItem,
            datePicker
        }
    }
</script>


<style>
    #todo-list {
        padding-left: 0px;
        margin-top: 5px;
        position: absolute;
        width: 100%;
    }

    #list {
        padding-left: 1px;
        margin-bottom: 0px;
        overflow-y: scroll;
        height: inherit;
    }

    #itemList {
        margin-top: 5px;
        overflow: hidden;
        background-color: rgba(0, 0, 0, 0);
        position: absolute;
        width: 100%;

    }

    ::-webkit-scrollbar {
        width: 0px; /* remove scrollbar space */

    }

    #todoAdd {
        margin-bottom: 5px;
        background-color: white;
    }

    #addDiv {
        background-color: white;
        border-style: solid;
        border-color: black;
        border-width: 1px;
        width: 100%;
        position: absolute;
        z-index: 5;
        margin-top: 5px;
    }

    #viewButton {
        width: 100%;
        display: block;
        background-color: #ffdb4d;
        margin: auto;
        border-style: dashed;
        border-color: black;
        border-width: 1px;

    }

    #viewButton:focus {
        outline: none;
    }

    #create {
        float: right;
    }

    input {
        margin-bottom: 3px;
    }

    .wrapper {
        opacity: 1;
        z-index: 5;
    }

</style>
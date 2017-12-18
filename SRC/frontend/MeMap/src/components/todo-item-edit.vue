<template>
    <div id="todoEdit">
        <div class='control'>

            <div class='btn-group todoControl btn-group-xs'>
                <button type="button" class="btn btn-default"
                        @click='submit'>
                    <span class='glyphicon glyphicon-ok'></span>
                </button>
                <button type="button" class="btn btn-default"
                        @click='cancel'>
                    <span class='glyphicon glyphicon-remove'></span>
                </button>
            </div>
        </div>
        <div>
            <form id="editForm">
                <input class="form-control" type="textaria" name="title"
                       :value='title' placeholder="Название заметки" maxlength="32">

                <date-picker id='datepicker' :value='date' :config="config"></date-picker>

                <input class="form-control" type="textaria" name="description"
                       :value='description' placeholder="Описание" maxlength="5000">

                <div class="input-group" style="{margin-bottom: 3px}">
                    <input class='form-control' type="textaria" name="address" placeholder="Выберите адрес на карте"
                           style="margin-bottom: 3px" :value='address' readonly='true'>
                    <span class="input-group-btn">
							        <button class="btn btn-secondary" type="button"
                                            @click='choosePlace'>Выбрать</button>
							    </span>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
    import datePicker from 'vue-bootstrap-datetimepicker';
    import 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.css';

    export default {
        name: 'todo-item-edit',
        props: {
            title: String,
            date: String,
            pos: Array,
            description: String,
            myMap: Object,
            address: String,
            id: Number,
            parentPlacemark: Object
        },
        components: {
            datePicker
        },
        data() {
            return {
                savePlacemark: '',
                editPlacemark: '',
                edit: true,
                callback: {},
                config: {
                    format: 'YYYY-MM-DD HH:mm',
                    useCurrent: false,
                    showClear: true,
                    showClose: true,
                    minDate: new Date(),
                    widgetPositioning: {
                        horizontal: 'right',
                        vertical: 'auto'
                    },
                },
            }
        },
        methods: {
            cancel(submit=false) {
                var item=null;
                if(submit===true) {
                    item={};
                    item.date = document.getElementById('datepicker').value;
                    item.description = document.querySelector('#editForm > .form-control:nth-child(3)').value;
                    item.title = document.querySelector('#editForm > .form-control:nth-child(1)').value;
                    item.address = this.address;
                    this.editPlacemark.properties
                        .set({
                            iconCaption: null,
                            balloonContent: null
                        });

                    item.coord=this.editPlacemark.geometry.getCoordinates();;
                }
                this.myMap.geoObjects.remove(this.editPlacemark);
                this.myMap.events.remove('click', this.callback);
                this.savePlacemark='';
                this.$emit('changeEdit',item);
            },
            submit() {
                let validate = function (item) {
                    if (item.header == '')
                        return false;
                    if (item.time == '')
                        return false;
                    let date = Date.parse(item.time);
                    if (date < Date.now())
                        return false;
                    return true;
                };
                let item = {};
                item.date = document.getElementById('datepicker').value;
                item.date = new Date(item.date).getTime();
                item.description = document.querySelector('#editForm > .form-control:nth-child(3)').value;
                item.header = document.querySelector('#editForm > .form-control:nth-child(1)').value;
                item.id=this.id;
                item.is_archived="";
                item.pos = this.editPlacemark.geometry.getCoordinates();
                if (validate(item)) {
                    let self = this;
                    $.ajax({
                        url: 'https://memap.ddns.net/api/notes/'+item.id+'?' + $.param({
                            token: localStorage.getItem('token'),
                            header: item.header,
                            date: item.date,
                            lattitude: item.pos[0],
                            longitude: item.pos[1],
                            description: item.description,
                            is_archived: item.is_archived
                        }),
                        method: 'PUT',
                        success(data) {
                            if (data.ok == true) {
                                self.cancel(true);
                            }
                            else
                                console.log('неверная заметка');
                        },
                        error(err) {
                        }
                    });
                }
            },
            choosePlace(){
                let self = this;
                ymaps.ready(function(){
                    self.callback = function (e) {
                        var coords = e.get('coords');
                        self.location = coords;
                        if (self.editPlacemark) {
                            self.editPlacemark.geometry.setCoordinates(coords);
                        } // Если нет – создаем.
                        else {
                            self.editPlacemark = new ymaps.Placemark(coords);
                            self.myMap.geoObjects.add(self.editPlacemark);
                        }
                        self.editPlacemark.item = self;

                        ymaps.geocode(coords).then(function (res) {
                            var firstGeoObject = res.geoObjects.get(0);
                            self.address=firstGeoObject.properties.get('name');
                            self.editPlacemark.properties
                                .set({
                                    iconCaption: firstGeoObject.properties.get('name'),
                                    balloonContent: firstGeoObject.properties.get('name')
                                });

                        });

                    };
                    self.myMap.events.add('click', self.callback);
                });
            }
        },
        mounted() {
            let date = document.getElementById('datepicker');
            date.value = this.date;

            this.myMap.geoObjects.remove(this.parentPlacemark);
            this.editPlacemark = new ymaps.Placemark(this.pos);
            this.myMap.geoObjects.add(this.editPlacemark);
        }
    }
</script>

<style>

</style>
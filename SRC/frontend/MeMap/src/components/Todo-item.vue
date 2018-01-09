<template>

    <div class='todo-item' :id='"id" + id' @click='viewMarker' @mouseover='showControls' @mouseleave='hideControls'>
        <div v-if="!edit">
            <div class='control'>

                <div v-if='visible' class='btn-group todoControl btn-group-xs'>
                    <button type="button" class="btn btn-default"
                            @click='doneItem'>
                        <span class='glyphicon glyphicon-ok'></span>
                    </button>
                    <button type="button" class="btn btn-default"
                            @click='edit = !edit'>
                        <span class='glyphicon glyphicon-pencil'></span>
                    </button>
                    <button type="button" class="btn btn-default"
                            @click='deleteItem'>
                        <span class='glyphicon glyphicon-remove'></span>
                    </button>
                </div>
            </div>
            <p>
                <span class="glyphicon glyphicon-tags"></span>
                {{' ' + title}}
            </p>
            <p>
                <span class="glyphicon glyphicon-calendar"></span>
                Дата и время: {{formattedDate}}
            </p>
            <p>
                <span class="glyphicon glyphicon-home"></span>
                Адрес: {{Adress}}
            </p>
            <p v-if='description && !isDescrLong' class='dropup'>
                <span class="glyphicon glyphicon-list-alt"></span>
                {{description}}
                <a v-if='showSpoiler' @click='isDescrLong = !isDescrLong'> <span class="caret"></span> </a>
            </p>
            <p v-else-if='description && isDescrLong'>
                <span class="glyphicon glyphicon-list-alt"></span>
                {{descr}}
                <a v-if='showSpoiler' @click='isDescrLong = !isDescrLong'> <span class="caret"></span> </a>
            </p>
        </div>
        <div v-else>
            <todo-item-edit
                    :title='title'
                    :pos='pos'
                    :address='Adress'
                    :date='formattedDate'
                    :description='description'
                    :myMap='myMap'
                    :id='id'
                    :parentPlacemark = 'pm'
                    :coordOptions="options"
                    @changeEdit="changeEdit">
            </todo-item-edit>
        </div>
    </div>

</template>

<script>
    import todoItemEdit from './Todo-item-edit.vue';

    export default {
        props: {
            title: String,
            pos: Array,
            time: Number,
            description: String,
            myMap: Object,
            adress: String,
            id: Number
        },

        data() {
            return {
                formattedDate: "",
                visible: false,
                Adress: "",
                options: {
                    results: 1,
                    json: true,
                    kind: 'house'
                },
                descr: "",
                isDescrLong: false,
                showFullDescr: false,
                showSpoiler: false,
                pm: '',
                edit: false
            }
        },
        components: {
            'todo-item-edit': todoItemEdit,
        },
        methods: {
            changeEdit(item) {
                if (item !== null) {
                    this.title = item.title;
                    this.description = item.description;
                    this.Adress = item.address;
                    this.formattedDate = item.date;
                    this.pm=new ymaps.Placemark(item.coord);
                }
                this.myMap.geoObjects.add(this.pm);
                this.edit = false;
            },
            deleteItem() {
                this.myMap.geoObjects.remove(this.pm);
                this.$emit('deleteItem', this.id);
            },
            doneItem() {
                this.myMap.geoObjects.remove(this.pm);
                this.$emit('doneItem', this.id);
            },
            viewMarker() {
                let self = this;
                ymaps.geoQuery(this.myMap.geoObjects)
                    .each(function (pm) {

                        if (pm.geometry._coordinates[0] == self.pos[0] && pm.geometry._coordinates[1] == self.pos[1]) {
                            pm.options.set('preset', 'islands#yellowIcon')
                            self.myMap.panTo(self.pos);
                        }
                        else
                            pm.options.set('preset', 'islands#blueIcon')
                    });
                let list = document.getElementById('list');
                for (var i in list.children) {
                    if (list.children[i].id) {
                        if (list.children[i].id == ('id' + self.id)) {
                            list.children[i].style['border-color'] = 'green';

                        }
                        else
                            list.children[i].style['border-color'] = '#ffdb4d';
                    }
                }
            },
            showControls() {
                if (!this.visible)
                    this.visible = !this.visible;
            },
            hideControls() {
                this.visible = !this.visible;
            }
        },
        mounted() {
            var self = this;
            var timer = setInterval(function () {
                if (ymaps.Placemark && self.myMap !== undefined) {
                    ymaps.geocode(self.pos, self.options)
                        .then((res) =>
                                self.Adress = res.GeoObjectCollection.featureMember[0].GeoObject.name,
                            (err) =>
                                console.log(err));
                    self.pm = new ymaps.Placemark(self.pos);
                    //self.pm.item = self;
                    self.pm.events.add('click', function (e) {
                        ymaps.geoQuery(self.myMap.geoObjects)
                            .each(function (pm) {
                                pm.options.set('preset', 'islands#blueIcon');
                            });
                        self.$emit('scrollTo', self.id)
                        self.pm.options.set('preset', 'islands#yellowIcon');
                        self.myMap.panTo(self.pos);
                        let list = document.getElementById('list');
                        for (var i in list.children) {
                            if (list.children[i].id) {
                                if (list.children[i].id == ('id' + self.id)) {
                                    list.children[i].style['border-color'] = 'green';
                                }
                                else
                                    list.children[i].style['border-color'] = '#ffdb4d';
                            }
                        }
                    });
                    self.myMap.geoObjects.add(self.pm);

                    clearInterval(timer);
                }
            }, 200);
            if (this.formattedDate === '') {
                let tempDate = new Date(this.time);
                let day = ('0' + tempDate.getDate()).substr(-2);
                let month = ('0' + (tempDate.getMonth() + 1)).substr(-2);
                let year = ('' + tempDate.getFullYear()).substr(-4);
                let hours = ('0' + tempDate.getHours()).substr(-2);
                let minutes = ('0' + tempDate.getMinutes()).substr(-2);
                this.formattedDate =year+'-'+ month+'-'+day+' ' +hours + ':' + minutes;
            }
            if (this.description && this.description.length > 50) {

                this.isDescrLong = true;
                this.showSpoiler = true;
                this.descr = this.description.substr(0, 50);
            }
        },
    }
</script>

<style>
    .todo-item {

        border-style: solid;
        border-width: 1px;
        border-color: #ffdb4d;

        background-color: white;
        margin: 0px;
        margin-bottom: 10px;
        padding: 4px;

    }

    .todoControl {
        float: right;

    }

    .control {
        margin-bottom: 10px;
        margin-top: 0px;
        position: relative;
        right: 5px;

    }

    p {
        margin-left: 10px;
        word-wrap: break-word;
    }

    .glyphicon-tags, .glyphicon-calendar, .glyphicon-home, .glyphicon-list-alt {
        margin-right: 5px;
    }
</style>
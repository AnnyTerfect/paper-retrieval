<template>
	<v-card class="ma-0" flat>
		<v-card-title>
			<span class="text-h5">Filter</span>
			<v-spacer></v-spacer>
			<v-btn icon @click="clickedShowNav" class="d-lg-none">
				<v-icon>
					{{ $store.state.showNav ? 'mdi-arrow-left' : 'mdi-arrow-right' }}
				</v-icon>
			</v-btn>
		</v-card-title>

		<v-divider></v-divider>

		<v-card-text>
			<div class="d-flex flex-wrap">
				<v-checkbox class="mt-0 mx-2" v-for="conference in $store.state.conferenceList" v-model="selectedConference"
					:label="conference" :value="conference" :key="conference"
					@change="updateSelectedConference"></v-checkbox>
			</div>
			<v-btn class="mt-2 mx-2" @click="selectAllConference">
				Select all
			</v-btn>
			<v-btn class="mt-2 mx-2" @click="unSelectAllConference">
				Unselect all
			</v-btn>
		</v-card-text>

		<v-divider></v-divider>

		<v-card-text class="pb-0">
			<v-text-field v-model="titleSearch" label="Search title" prepend-icon="mdi-card-text"
				append-outer-icon="mdi-magnify" :append-icon="titleSearch != '' ? 'mdi-close' : ''"
				@click:append="clearTitleSearch" @input="updateTitleSearch"></v-text-field>
		</v-card-text>

		<v-card-text class="py-0">
			<v-text-field v-model="authorSearch" label="Search author" prepend-icon="mdi-account"
				append-outer-icon="mdi-magnify" :append-icon="authorSearch != '' ? 'mdi-close' : ''"
				@click:append="clearAuthorSearch" @input="updateAuthorSearch"></v-text-field>
		</v-card-text>

		<v-divider></v-divider>

		<v-card-text>
			<span class="mr-2">Title exclude:</span>
			<v-chip close v-for="(title, index) in titleExclude" :key="index" @click:close="removeTitleExclude(index)"
				class="mb-1 mr-1">
				{{ title }}
			</v-chip>

			<v-text-field v-model="newTitleExclude" label="Add" append-outer-icon="mdi-plus"
				@keypress.enter="addNewTitleExclude"></v-text-field>
		</v-card-text>

		<v-card-text>
			<span class="mr-2">Title include:</span>
			<v-chip close v-for="(title, index) in titleInclude" :key="index" @click:close="removeTitleInclude(index)"
				class="mb-1 mr-1">
				{{ title }}
			</v-chip>

			<v-text-field v-model="newTitleInclude" label="Add" append-outer-icon="mdi-plus"
				@keypress.enter="addNewTitleInclude"></v-text-field>
		</v-card-text>

		<v-card-text>
			<span class="mr-2">Author exclude:</span>
			<v-chip close v-for="(author, index) in authorExclude" :key="index" @click:close="removeAuthorExclude(index)"
				class="mb-1 mr-1">
				{{ author }}
			</v-chip>

			<v-text-field v-model="newAuthorExclude" label="Add" append-outer-icon="mdi-plus"
				@keypress.enter="addNewAuthorExclude"></v-text-field>
		</v-card-text>

		<v-card-text>
			<span class="mr-2">Author include:</span>
			<v-chip close v-for="(author, index) in authorInclude" :key="index" @click:close="removeAuthorInclude(index)"
				class="mb-1 mr-1">
				{{ author }}
			</v-chip>

			<v-text-field v-model="newAuthorInclude" label="Add" append-outer-icon="mdi-plus"
				@keypress.enter="addNewAuthorInclude"></v-text-field>
		</v-card-text>

		<v-card-text>
			<span class="mr-2">Abstract exclude:</span>
			<v-chip close v-for="(abstract, index) in abstractExclude" :key="index"
				@click:close="removeAbstractExclude(index)" class="mb-1 mr-1">
				{{ abstract }}
			</v-chip>

			<v-text-field v-model="newAbstractExclude" label="Add" append-outer-icon="mdi-plus"
				@keypress.enter="addNewAbstractExclude"></v-text-field>
		</v-card-text>
	</v-card>
</template>

<script>
import axios from 'axios'

export default {
	name: 'MyFilter',

	data: () => ({
		titleSearch: '',
		authorSearch: '',

		selectedConference: [],

		newAuthorExclude: '',
		newAuthorInclude: '',
		newTitleExclude: '',
		newTitleInclude: '',
		newAbstractExclude: '',

		titleExclude: ['gan', 'transformer', 'generation', 'vision', 'visual', 'voice', 'adversarial', 'image', '3d', 'video', 'pixel', 'media', 'render', 'network', 'language', 'deep', 'encod', 'gnn', 'graph', 'all you need', 'hyperparameter', 'distillation', 'greedy', 'text', 'sequence', 'attention', 'detection', 'physic', 'chemical', 'rnn', 'recurrent', 'vit', 'token', 'embedding', 'agent', 'mlp', 'tensor', 'federate', 'net', 'navigat', 'atari', 'training', 'cloud', 'vae', 'pose', 'robot', 'tuning', 'pretrain', 'motion', 'recommend'],
		titleInclude: ['theory', 'regret', 'bound', 'optimal', 'theor'],
		authorExclude: ['zhaoran'],
		authorInclude: ['zhi-hua'],
		abstractExclude: ['voice', 'adversarial', 'image', 'video', 'pixel', 'media', 'render', 'distillation', 'physic', 'chemical', 'federate', 'navigat', 'atari', 'recurrent', 'position', 'graph', 'embedding', 'hyperparameter', 'language', 'transformer', 'generative', 'nlp'],
	}),

	mounted: function () {
		this.getConfList()
		this.$store.commit('receiveTitleExclude', {
			titleExclude: this.titleExclude
		})
		this.$store.commit('receiveTitleInclude', {
			titleInclude: this.titleInclude
		})
		this.$store.commit('receiveAuthorExclude', {
			authorExclude: this.authorExclude
		})
		this.$store.commit('receiveAuthorInclude', {
			authorInclude: this.authorInclude
		})
		this.$store.commit('receiveAbstractExclude', {
			abstractExclude: this.abstractExclude
		})
	},

	methods: {
		clickedShowNav() {
			this.$store.commit('receiveUpdateShowNav', {
				showNav: !this.$store.state.showNav
			})
		},
		getConfList() {
			axios.get('/api/getConfList')
				.then((res) => {
					let conferenceList = res.data.sort()
					this.$store.commit('receiveConferenceList', {
						conferenceList
					})
					this.selectAllConference()
				})
				.catch((err) => {
					console.log(err)
				})
		},
		updateSelectedConference() {
			this.$store.commit('receiveSelectedConference', {
				selectedConference: this.selectedConference
			})
		},
		selectAllConference() {
			this.selectedConference = this.$store.state.conferenceList
			this.updateSelectedConference()
		},
		unSelectAllConference() {
			this.selectedConference = []
			this.updateSelectedConference()
		},
		clearTitleSearch: function () {
			this.titleSearch = ''
			this.updateTitleSearch()
		},
		clearAuthorSearch: function () {
			this.authorSearch = ''
			this.updateAuthorSearch()
		},
		updateTitleSearch: function () {
			this.$store.commit('receiveTitleSearch', {
				titleSearch: this.titleSearch
			})
		},
		updateAuthorSearch: function () {
			this.$store.commit('receiveAuthorSearch', {
				authorSearch: this.authorSearch
			})
		},
		addNewTitleExclude: function () {
			this.titleExclude.push(this.newTitleExclude)
			this.$store.commit('receiveTitleExclude', {
				titleExclude: this.titleExclude
			})
			this.newTitleExclude = ''
		},
		addNewTitleInclude: function () {
			this.titleInclude.push(this.newTitleInclude)
			this.$store.commit('receiveTitleInclude', {
				titleInclude: this.titleInclude
			})
			this.newTitleInclude = ''
		},
		removeTitleExclude: function (index) {
			this.titleExclude.splice(index, 1)
			this.$store.commit('receiveTitleExclude', {
				titleExclude: this.titleExclude
			})
		},
		removeTitleInclude: function (index) {
			this.titleInclude.splice(index, 1)
			this.$store.commit('receiveTitleInclude', {
				titleInclude: this.titleInclude
			})
		},
		addNewAuthorExclude: function () {
			this.authorExclude.push(this.newAuthorExclude)
			this.$store.commit('receiveAuthorExclude', {
				authorExclude: this.authorExclude
			})
			this.newAuthorExclude = ''
		},
		addNewAuthorInclude: function () {
			this.authorInclude.push(this.newAuthorInclude)
			this.$store.commit('receiveAuthorInclude', {
				authorInclude: this.authorInclude
			})
			this.newAuthorInclude = ''
		},
		removeAuthorExclude: function (index) {
			this.authorExclude.splice(index, 1)
			this.$store.commit('receiveAuthorExclude', {
				authorExclude: this.authorExclude
			})
		},
		removeAuthorInclude: function (index) {
			this.authorInclude.splice(index, 1)
			this.$store.commit('receiveAuthorInclude', {
				authorInclude: this.authorInclude
			})
		},
		addNewAbstractExclude: function () {
			this.abstractExclude.push(this.newAbstractExclude)
			this.$store.commit('receiveAbstractExclude', {
				abstractExclude: this.abstractExclude
			})
			this.newAbstractExclude = ''
		},
		removeAbstractExclude: function (index) {
			this.abstractExclude.splice(index, 1)
			this.$store.commit('receiveAbstractExclude', {
				abstractExclude: this.abstractExclude
			})
		},
	},
}
</script>
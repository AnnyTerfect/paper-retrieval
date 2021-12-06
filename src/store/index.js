import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    titleSearch: '',
    authorSearch: '',
    titleExclude: [],
    titleInclude: [],
    authorExclude: [],
    authorInclude: [],
    abstractExclude: [],
    showNav: true,
  },
  mutations: {
    receiveTitleSearch(state, payload) {
      state.titleSearch = payload.titleSearch
    },
    receiveAuthorSearch(state, payload) {
      state.authorSearch = payload.authorSearch
    },
    receiveTitleExclude(state, payload) {
      state.titleExclude = payload.titleExclude
    },
    receiveTitleInclude(state, payload) {
      state.titleInclude = payload.titleInclude
    },
    receiveAuthorExclude(state, payload) {
      state.authorExclude = payload.authorExclude
    },
    receiveAuthorInclude(state, payload) {
      state.authorInclude = payload.authorInclude
    },
    receiveAbstractExclude(state, payload) {
      state.abstractExclude = payload.abstractExclude
    },
    receiveUpdateShowNav(state, payload) {
      state.showNav = payload.showNav
    }
  },
  actions: {
  },
  modules: {
  }
})

<template>
  <v-app>
    <v-navigation-drawer
      app
      clipped
      width="350"
      max-width="100%"
      v-model="$store.state.showNav"
    >
      <paper-filter
      ></paper-filter>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="primary"
      dark
      clipped-left
    >
      <div class="d-flex align-center">
        <span class="text-h6 font-weight-regular">
          <v-icon class="mr-1">mdi-archive-search</v-icon>
          Paper Retrieval
        </span>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        icon
      >
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

import MyFilter from './components/MyFilter.vue'

export default {
  name: 'App',

  data: () => ({
  }),
  components: {
    'paper-filter': MyFilter
  }
};
</script>

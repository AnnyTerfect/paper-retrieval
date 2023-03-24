<template>
  <v-container fluid :class="{ 'fill-height': papers.length == 0 }">
    <v-layout class="align-center justify-center" v-if="!papers.length">
      <v-progress-circular indeterminate size="60" color="primary">
      </v-progress-circular>
    </v-layout>

    <v-expand-transition>
      <v-card class="mb-1" v-if="papers.length" v-show="showJump">
        <v-card-title class="pt-2 text-body-1">
          Jump page
        </v-card-title>
        <v-card-subtitle class="text-body-2">
          Page {{ page }} of {{ numberOfPages }}
        </v-card-subtitle>
        <v-card-text class="pb-0">
          <v-slider class="mt-5" v-model="page" step="1" min="1" :max="numberOfPages == 0 ? 1 : numberOfPages" thumb-label
            always-dirty dense>
            <template v-slot:prepend>
              <v-icon @click="page = page > 1 ? page - 1 : 1">
                mdi-minus
              </v-icon>
            </template>

            <template v-slot:append>
              <v-icon @click="page = page < numberOfPages ? page + 1 : numberOfPages">
                mdi-plus
              </v-icon>
            </template>
          </v-slider>
        </v-card-text>
      </v-card>
    </v-expand-transition>

    <v-layout class="align-center justify-center mb-2" v-if=papers.length>
      <v-btn icon @click="clickedShowNav">
        <v-icon>
          {{ $store.state.showNav ? 'mdi-chevron-left' : 'mdi-chevron-right' }}
        </v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon @click="showJump = !showJump">
        <v-icon>
          {{ showJump ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
        </v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon>
      </v-btn>
    </v-layout>

    <v-card>
      <v-data-iterator v-if="papers.length" :items="filteredPapers" :items-per-page.sync="itemsPerPage" :page.sync="page"
        sort-by="title" hide-default-footer ref="dataIterator">
        <template v-slot:default="props">
          <transition-group name="fade">
            <v-card v-for="(paper, index) in props.items" :key="paper.titleBase64" class="mb-1" flat>
              <v-divider v-if="index == 0" class="mb-1"></v-divider>
              <v-card-title class="text-subtitle-1 font-weight-bold pt-2 pb-0" style="line-height: 1.3em; display: block">
                {{ paper.title }}
                <span
                  v-if="$store.state.selectedConference.length > 1"
                  class="grey--text ml-2"
                >
                  {{ paper.conf }}
                </span>
              </v-card-title>
              
              <v-card-subtitle class="text-subtitle-2 pt-4 pb-0 d-lg-none">
                {{ paper.authors }}
              </v-card-subtitle>

              <v-card-actions class="pt-0 px-4">
                <span class="text-body-2 d-none d-lg-inline">
                  {{ paper.authors }}
                </span>

                <v-spacer></v-spacer>

                <v-btn text x-small plain @click="downloadAll(paper.titleBase64)" class="text-overline black--text">
                  ALL
                </v-btn>

                <!--<v-btn
                  text
                  @click="download(paper.titleBase64)"
                >
                  DOWNLOAD PDF
                </v-btn>-->

                <v-btn text x-small plain @click="view(paper.titleBase64)" class="text-overline black--text">
                  PDF
                </v-btn>

                <v-btn text x-small plain @click="paper.expanded = !paper.expanded" class="text-overline black--text">
                  ABSTRACT<v-icon>{{ paper.expanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </v-btn>
              </v-card-actions>

              <v-expand-transition>
                <div v-show="paper.expanded">
                  <v-divider></v-divider>

                  <v-card-text class="text-body-2">
                    {{ paper.abstract }}
                  </v-card-text>
                </div>
              </v-expand-transition>

              <v-divider class="my-1"></v-divider>
            </v-card>
          </transition-group>
        </template>

        <template v-slot:footer>
          <v-card flat class="mt-2 d-flex" align="center" justify="center">
            <v-card-text class="d-flex align-center">
              <span class="grey--text">Items per page</span>
              <v-menu offset-y>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn dark text color="primary" class="ml-2" v-bind="attrs" v-on="on">
                    {{ itemsPerPage }}
                    <v-icon>mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item v-for="(number, index) in itemsPerPageArray" :key="index"
                    @click="updateItemsPerPage(number)">
                    <v-list-item-title>{{ number }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>

              <v-spacer></v-spacer>

              <span class="mr-4
                    grey--text">
                Page {{ page }} of {{ numberOfPages }}
              </span>
              <v-btn fab small dark color="blue darken-3" class="mr-1" @click="formerPage" :disabled="page === 1">
                <v-icon color="primary">mdi-chevron-left</v-icon>
              </v-btn>
              <v-btn fab small dark color="blue darken-3" class="ml-1" @click="nextPage" :disabled="page === numberOfPages">
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-card-text>
          </v-card>
        </template>
      </v-data-iterator>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ViewPaper',

  data: () => ({
    papers: [],
    itemsPerPageArray: [10, 20, 50, 100, 200, 500],
    filter: {},
    page: 1,
    itemsPerPage: 20,
    showJump: true,
  }),

  computed: {
    filteredPapers() {
      return this.papers.filter((paper) => {
        let conf = paper.conf
        let title = paper.title.toLowerCase()
        let author = paper.authors.toLowerCase()
        let abstract = paper.abstract.toLowerCase()

        let titleSearch = this.$store.state.titleSearch.toLowerCase()
        let authorSearch = this.$store.state.authorSearch.toLowerCase()
        let titleExclude = this.$store.state.titleExclude
        let titleInclude = this.$store.state.titleInclude
        let authorExclude = this.$store.state.authorExclude
        let authorInclude = this.$store.state.authorInclude
        let abstractExclude = this.$store.state.abstractExclude

        if (this.$store.state.selectedConference.indexOf(conf) < 0) {
          return false
        }

        if (titleSearch && title.indexOf(titleSearch) < 0)
          return false

        if (authorSearch && author.indexOf(authorSearch) < 0)
          return false

        for (let i = 0; i < titleInclude.length; i++) {
          let titIn = titleInclude[i].toLowerCase()
          if (title.indexOf(titIn) >= 0)
            return true
        }

        for (let i = 0; i < titleExclude.length; i++) {
          let titEx = titleExclude[i].toLowerCase()
          if (title.indexOf(titEx) >= 0)
            return false
        }

        for (let i = 0; i < authorInclude.length; i++) {
          let autIn = authorInclude[i].toLowerCase()
          if (RegExp(`(^${autIn} )|( ${autIn} )|( ${autIn},)|( ${autIn}$)`).exec(author))
            return true
        }

        for (let i = 0; i < authorExclude.length; i++) {
          let autEx = authorExclude[i].toLowerCase()
          if (RegExp(`(^${autEx} )|( ${autEx} )|( ${autEx},)|( ${autEx}$)`).exec(author))
            return false
        }

        for (let i = 0; i < abstractExclude.length; i++) {
          let absEx = abstractExclude[i].toLowerCase()
          if (abstract.indexOf(absEx) >= 0)
            return false
        }
        return true
      })
    },

    numberOfPages() {
      return Math.ceil(this.filteredPapers.length / this.itemsPerPage)
    },
  },

  mounted: function () {    
    this.getPapers()
  },

  methods: {
    clickedShowNav() {
      this.$store.commit('receiveUpdateShowNav', {
        showNav: !this.$store.state.showNav
      })
    },
    getPapers() {
      let _this = this
      this.papers = []
      
      axios.get('/api/getPapers')
        .then((res) => {
          let data = res.data

          for (let i = 0; i < data.length; i++) {
            data[i].expanded = false
            data[i].title = data[i].title.replace(' -', ':')
            _this.papers.push(data[i])
          }
        })
        .catch((err) => {
          console.log(err)
        })
    },
    nextPage() {
      if (this.page + 1 <= this.numberOfPages) {
        this.$vuetify.goTo(this.$refs.dataIterator, { duration: 300 })

        setTimeout(() => {
          this.page += 1
        }, 300)
      }
    },
    formerPage() {
      if (this.page - 1 >= 1) {
        this.$vuetify.goTo(this.$refs.dataIterator, { duration: 300 })

        setTimeout(() => {
          this.page -= 1
        }, 300)
      }
    },
    updateItemsPerPage(number) {
      this.itemsPerPage = number
    },
    view(titleBase64) {
      window.open('/view/' + titleBase64)
    },
    download(titleBase64) {
      window.open('/download/' + titleBase64)
    },
    downloadAll(titleBase64) {
      window.open('/downloadAll/' + titleBase64)
    },
  }
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: all .5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
import Vue from 'vue';
import Vuex, {StoreOptions} from 'vuex';
import {mainModule} from './state';
import {ydlItemModule} from './ytdl_item';

import {State} from './state';

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    ydlItem: ydlItemModule,

  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;

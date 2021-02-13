import {getStoreAccessors} from 'typesafe-vuex';
import {State} from '../state';
import {YdlItemListState, YdlItemState} from './state';

export const getters = {

    getYtdItems: (state: YdlItemListState) => state.ydlItems.sort((a, b) => (a.id > b.id) ? 1 : -1),

    getYtdItem: (state: YdlItemListState) => (id: number) => {
        const filterQuery = state.ydlItems.filter((query: YdlItemState) => query.id === id);
        if (filterQuery.length > 0) {
            return {...filterQuery[0]}
        }
    },

}

const {read} = getStoreAccessors<YdlItemListState, State>('');

export const readAllYtdItems = read(getters.getYtdItems);
export const readYtdItem = read(getters.getYtdItem);


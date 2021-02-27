import {getStoreAccessors} from 'typesafe-vuex';
import {State} from '../state';
import {YdlItemState, YdlItemListState, YdlUrlInfoCreate} from './state';

export const mutations = {

    setYdlItems(state: YdlItemListState, payload: YdlItemState[]) {
        state.ydlItems = payload;
    },
    setYdlItem(state: YdlItemListState, payload: YdlItemState) {
        const queries = state.ydlItems.filter((query: YdlItemState) => query.id != payload.id);
        queries.push(payload);
        state.ydlItems = queries;
    },
    setYdlUrlInfo(state: YdlItemListState, payload: {}) {
        state.ydlUrlInfo = payload;
    },
    removeYdlItem(state: YdlItemListState, payload: { id: 0 }) {
        state.ydlItems = state.ydlItems.filter((query: YdlItemState) => query.id != payload.id);
    }

};

const {commit} = getStoreAccessors<YdlItemListState, State>('');

export const commitSetYdlItems = commit(mutations.setYdlItems);
export const commitSetYdlItem = commit(mutations.setYdlItem);
export const commitRemoveYdlItem = commit(mutations.removeYdlItem);
export const commitSetYdlUrlInfo = commit(mutations.setYdlUrlInfo);

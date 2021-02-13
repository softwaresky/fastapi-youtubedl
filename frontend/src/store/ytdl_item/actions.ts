import {ActionContext} from 'vuex';
import {getStoreAccessors} from 'typesafe-vuex';
import {api} from '@/api';
import {State} from '../state';
import {YdlItemState, YdlItemListState, YdlItemCreate, YdlItemUpdate} from './state';
import {commitSetYdlItem, commitSetYdlItems, commitRemoveYdlItem} from './mutations';

type MainContext = ActionContext<YdlItemListState, State>;

export const actions = {

    async actionGetYdlItems(context: MainContext) {
        try {
            const response = await api.getYdlItems();
            if (response) {
                commitSetYdlItems(context, response.data);
            }
        } catch (error) {
            console.log(error);
        }
    },
    async actionCreateYdlItem(context: MainContext, payload: YdlItemCreate) {

        try {
            const response = await api.createYdlItem(payload);
            if (response) {
                commitSetYdlItem(context, response.data);
            }

        } catch (error) {
            console.log(error);
        }
    },
    async actionUpdateYdlItem(context: MainContext, payload: { id: number; ydlItem: YdlItemState }) {
        try {

            const response = await api.updateYdlItem(payload.id, payload.ydlItem);
            if (response) {
                commitSetYdlItem(context, response.data);
            }
        } catch (error) {
            console.log(error);
        }
    },
    async actionRemoveYdlItem(context: MainContext, payload: { id: number}) {
        try {
            const response = await api.removeYdlItem(payload.id);
            if (response) {
                commitRemoveYdlItem(context, response.data);
            }

        } catch (error) {
            console.log(error);
        }
    },

};

const {dispatch} = getStoreAccessors<YdlItemListState, State>('');

export const dispatchGetYdlItems = dispatch(actions.actionGetYdlItems);
export const dispatchCreateYdlItem = dispatch(actions.actionCreateYdlItem);
export const dispatchUpdateYdlItem = dispatch(actions.actionUpdateYdlItem);
export const dispatchRemoveYdlItem = dispatch(actions.actionRemoveYdlItem);


import {actions} from "./actions";
import {getters} from './getters';
import {mutations} from './mutations';
import {YdlItemState, YdlItemListState} from './state';

const defaultState: YdlItemListState = {
    ydlItems: [],
};

export const ydlItemModule = {
    state: defaultState,
    mutations,
    actions,
    getters
}

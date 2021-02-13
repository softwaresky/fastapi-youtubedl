export interface State {
    version: string;
}


const defaultState: State = {
    version: "1.0.0",
};

export const mainModule = {
    state: defaultState,

}

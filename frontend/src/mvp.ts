export interface IModel {
    getPresenter(): IPresenter
    startSoloGame(): void;
    startDuelGame(): void;
    sendLetter(letter: string): void;
    removeLetter(): void;
    publishWord(): void;
}

export interface IViewManager {
    getPresenter(): IPresenter;
    duelView(): IDuelView;
    menuView(): IMenu;
    accept(action: ViewAction): void;
}

export interface IPresenter {
    run() : void;
    accept(action: ViewAction): void;
    acceptData(action: ModelAction, data: string): void;
}

export interface IView {
    remove(): void;
    getManager(): IViewManager;
}

export interface IDuelView extends IView {
    renderGame(data: any): void;
    renderChanges(data: any): void;
}

export interface IMenu extends IView {
    
}

export enum ViewAction {
    START_SOLO,
    START_DUEL,
}

export enum ModelAction {
    RENDER_ALL,
    RENDER_CHANGE,
}

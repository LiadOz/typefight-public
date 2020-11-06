export interface IModel {
    
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
}

export interface IView {
    remove(): void;
    getManager(): IViewManager;
}

export interface IDuelView extends IView {
    addWord(): void;
    removeWord(): void;
}

export interface IMenu extends IView {
    
}

export enum ViewAction {
    START_SOLO,
}

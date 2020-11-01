"use strict";
exports.__esModule = true;
exports.Presenter = void 0;
var view_1 = require("view/view");
var model_1 = require("model/model");
var Presenter = /** @class */ (function () {
    function Presenter(container) {
        this.model = new model_1.Model;
        this.view = new view_1.ViewFactory().create('PIXI', container);
    }
    Presenter.prototype.run = function () {
        this.view.initView();
    };
    return Presenter;
}());
exports.Presenter = Presenter;

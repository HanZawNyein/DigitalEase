import {Component, xml} from "@odoo/owl";

// -------------------------------------------------------------------------
// Root Component
// -------------------------------------------------------------------------
export default class Root extends Component {
    static template = xml/* xml */
        `<div>
            Hello
        </div>`;
}
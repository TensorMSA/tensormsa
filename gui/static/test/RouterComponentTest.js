import React from 'react';
import TestUtils from 'react-addons-test-utils';
import RouterComponent from '../js/RouterComponent';
import expect from 'expect';

describe("RouterComponent", function() {
    it("should shallow render without errors", () => {
        let renderer = TestUtils.createRenderer();
        renderer.render(<RouterComponent/>);
        let result = renderer.getRenderOutput();
    });
});
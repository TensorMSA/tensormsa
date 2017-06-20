import React from 'react'
import TestUtils from 'react-addons-test-utils'
import {findRenderedDOMComponentWithClass as find} from 'react-addons-test-utils'
import {scryRenderedDOMComponentsWithClass as findAll} from 'react-addons-test-utils'
import HomeComponent from './../js/HomeComponent'
import expect from 'expect'
import NN_InfoListComponent from './../js/NNConfiguration/NN_InfoListComponent'

describe("HomeComponent", function() {
    let renderer = TestUtils.createRenderer();
    renderer.render(<HomeComponent/>);
  	let result = renderer.getRenderOutput();

    it("should display Initialize NN", () => {
        let instance = renderer.getMountedInstance();
        expect(instance.state.NN_InfoList).toBe(null);
    });

    it("should display InfoList NN", () => {
        let instance = renderer.getMountedInstance();
        instance.getNetInfo();
        expect(instance.state.NN_InfoList).toInclude(<NN_InfoListComponent/>);
    });

    it("should display NN Information List", () => {
    //    TestUtils.Simulate.click(find('getAPI'));
    //     expect(result.type).toBe('div');
    });

    it("should display Create Data Table", () => {
     //  TestUtils.Simulate.click(find('getAPI'));
     //  expect(result.type).toBe('div');
    });

    it("should display Search Data Table", () => {
     //  TestUtils.Simulate.click(find('getAPI'));
     //  expect(result.type).toBe('div');
    });
});
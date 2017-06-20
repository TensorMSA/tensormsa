import React from 'react'
import TestUtils from 'react-addons-test-utils'
import {findRenderedDOMComponentWithClass as find} from 'react-addons-test-utils'
import {scryRenderedDOMComponentsWithClass as findAll} from 'react-addons-test-utils'
import HomeComponent from './../../js/HomeComponent'
import expect from 'expect'
import NN_InfoListComponent from './../../js/NNConfiguration/NN_InfoListComponent'
import NN_BasicInfoComponent from './../../js/NNConfiguration/NN_BasicInfoComponent'

describe("NN_InfoListComponent", function() {
    let renderer = TestUtils.createRenderer();
    renderer.render(<HomeComponent/>);
  	let result = renderer.getRenderOutput();
    let instance = renderer.getMountedInstance();
    instance.getNetInfo();

    it("should display Add New NN", () => {
 //     TestUtils.Simulate.click(find(InfoListComponent,'add'));
        expect(result.props.children).toInclude(<NN_BasicInfoComponent />);
    });
});
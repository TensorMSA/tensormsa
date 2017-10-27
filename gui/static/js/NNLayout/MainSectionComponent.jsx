import React from 'react'

export default class MainSectionComponent extends React.Component {
    render() {
        return (   
                <section>
	            	<div className="main_visual_area">
						<div><img src="./../templates/images/main_visual01.png" alt="" />
						</div>
						<div className="visual_txt_area">
							<p className="visual_txt">
								<strong>TensorMSA is Machine Learning API</strong>
								MicroServiceArchitecthre with Python and Tensorflow
							</p>
						</div>
					</div>
					<div className="main_contents_area">
						<div className="notice_area">
							<div className="main_con_title">
								Info
								<a href="#none">+ more</a>
							</div>
							<div className="table_area">
								<table>
									<thead>
										<tr>
											<th scope="col">No</th>
											<th scope="col">Title</th>
											<th scope="col">Day</th>
										</tr>
									</thead>
									<tbody>
										<tr>
											<td>1</td>
											<td><a href="http://hugrypiggykim.com/">TensorMSA Home Page</a></td>
											<td><span className="table_date">2017.09.29</span></td>
										</tr>
										<tr>
											<td>2</td>
											<td><a href="https://github.com/seungwookim">Github Page</a></td>
											<td><span className="table_date">-</span></td>
										</tr>
										<tr>
											<td>3</td>
											<td><a href="http://hugrypiggykim.com/about-hungry-piggy-kim/">About us</a></td>
											<td><span className="table_date">-</span></td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
						<div className="quick_menu_area">
							<div className="main_con_title">
								Support
								<a href="#none">+ more</a>
							</div>
							<div className="table_area">
								<table>
									<thead>
										<tr>
											<th scope="col">No</th>
											<th scope="col">Title</th>
										</tr>
									</thead>
									<tbody>
										<tr>
											<td>1</td>
											<td><a href="http://hugrypiggykim.com/2017/09/19/1237/">About TensorMSA</a></td>
											<td><span className="table_date">-</span></td>
										</tr>
										<tr>
											<td>2</td>
											<td><a href="http://hugrypiggykim.com/category/tensormsa-guide/development-environment/">Development Environment</a></td>
											<td><span className="table_date">-</span></td>
										</tr>
										<tr>
											<td>3</td>
											<td><a href="http://hugrypiggykim.com/2017/09/20/tensormsa-guide-rule-set-up/">Setup Configuration</a></td>
											<td><span className="table_date">-</span></td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
                </section>
        )
    }
}
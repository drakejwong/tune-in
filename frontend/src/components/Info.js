import React from 'react';

import {
    Button,
    Table
  } from "reactstrap";

class Info extends React.Component {

    render() {
        return (
        <>
            <Table responsive>
                <thead>
                    <tr>
                        <th className="text-center">#</th>
                        <th>Name</th>
                        <th>Job Position</th>
                        <th className="text-center">Since</th>
                        <th className="text-right">Salary</th>
                        <th className="text-right">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td className="text-center">1</td>
                        <td>Andrew Mike</td>
                        <td>Develop</td>
                        <td className="text-center">2013</td>
                        <td className="text-right">€ 99,225</td>
                        <td className="text-right">
                            <Button className="btn-icon" color="info" size="sm">
                                <i className="fa fa-user"></i>
                            </Button>{` `}
                            <Button className="btn-icon" color="success" size="sm">
                                <i className="fa fa-edit"></i>
                            </Button>{` `}
                            <Button className="btn-icon" color="danger" size="sm">
                                <i className="fa fa-times" />
                            </Button>
                        </td>
                    </tr>
                    <tr>
                        <td className="text-center">2</td>
                        <td>Manuel Rico</td>
                        <td>Manager</td>
                        <td className="text-center">2012</td>
                        <td className="text-right">€ 99,201</td>
                        <td className="text-right">
                            <Button className="btn-icon btn-round" color="info" size="sm">
                                <i className="fa fa-user"></i>
                            </Button>{` `}
                            <Button className="btn-icon btn-round" color="success" size="sm">
                                <i className="fa fa-edit"></i>
                            </Button>{` `}
                            <Button className="btn-icon btn-round" color="danger" size="sm">
                                <i className="fa fa-times" />
                            </Button>{` `}
                        </td>
                    </tr>
                    <tr>
                        <td className="text-center">3</td>
                        <td>Alex Mike</td>
                        <td>Designer</td>
                        <td className="text-center">2012</td>
                        <td className="text-right">€ 99,201</td>
                        <td className="text-right">
                            <Button className="btn-icon btn-simple" color="info" size="sm">
                                <i className="fa fa-user"></i>
                            </Button>{` `}
                            <Button className="btn-icon btn-simple" color="success" size="sm">
                                <i className="fa fa-edit"></i>
                            </Button>{` `}
                            <Button className="btn-icon btn-simple" color="danger" size="sm">
                                <i className="fa fa-times" />
                            </Button>{` `}
                        </td>
                    </tr>
                </tbody>
            </Table>
        </>
        );
    }
}

export default Info;
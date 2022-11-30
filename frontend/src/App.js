import logo from './logo.svg';
import './App.css';
import "bootstrap/dist/css/bootstrap.min.css"
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Routes,
  BrowserRouter,
  Link
} from "react-router-dom";

import Login from "./containers/Login"
import Dashboard from './containers/Dashboard';
import CreateUser from './containers/CreateUser'
import CreateBroker from './containers/CreateBroker';
import UserDetails from './containers/UserDetails';
import TransactionList from './containers/TransactionList'
import Logout from './containers/Logout';
import CreateManager from './containers/CreateManager';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/create-user" element={<CreateUser />} />
        <Route path="/create-broker" element={<CreateBroker />} />
        <Route path="/create-manager" element={<CreateManager />} />
        <Route path="/user-details/" element={<UserDetails />} />
        <Route path="/transaction-list/" element={<TransactionList />} />
        <Route path="/logout/" element={<Logout />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

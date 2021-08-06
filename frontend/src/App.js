import "./App.css";
import Layout from "./components/Layout";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import RemoveBgPage from "pages/RemoveBgPage";

function App() {
  return (
    <Router>
      <Layout>
        <Switch>
          <Route path="/" component={RemoveBgPage} exact />
        </Switch>
      </Layout>
    </Router>
  );
}

export default App;

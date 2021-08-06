import "./App.css";
import Layout from "./components/Layout";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import RemoveBgPage from "pages/RemoveBgPage";
import PortraitSketch from "pages/PortraitSketch";

function App() {
  return (
    <Router>
      <Layout>
        <Switch>
          <Route path="/" component={RemoveBgPage} exact />
          <Route path="/portrait-sketch" component={PortraitSketch} exact />
        </Switch>
      </Layout>
    </Router>
  );
}

export default App;

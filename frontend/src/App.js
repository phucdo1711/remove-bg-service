import "./App.css";
import Layout from "./components/Layout";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import RemoveBgPage from "pages/RemoveBgPage";
import PortraitSketch from "pages/PortraitSketch";
import StyleTransferPage from "pages/StyleTransferPage";
import Photo2Cartoon from "pages/Photo2Cartoon";

function App() {
  return (
    <Router>
      <Layout>
        <Switch>
          <Route path="/" component={RemoveBgPage} exact />
          <Route path="/portrait-sketch" component={PortraitSketch} exact />
          <Route path="/style-transfer" component={StyleTransferPage} exact />
          <Route path="/photo-to-cartoon" component={Photo2Cartoon} exact />
        </Switch>
      </Layout>
    </Router>
  );
}

export default App;

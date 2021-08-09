import { Layout, Menu, Breadcrumb } from "antd";
import styles from "./Layout.module.scss";
import logoImg from "assets/images/logo-white.svg";
import { Link } from "react-router-dom";

const { Header, Content, Footer } = Layout;

const MainLayout = ({ children }) => {
  return (
    <Layout className={styles.layout}>
      <Header>
        <div className={styles.logo}>
          <img src={logoImg} alt="Logo" />
        </div>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["/"]}>
          <Link to="/">
            <Menu.Item key="/">Remove Background</Menu.Item>
          </Link>
          <Link to="/portrait-sketch">
            <Menu.Item key="/portrait-sketch">Portrait Sketch</Menu.Item>
          </Link>
          <Link to="/style-transfer">
            <Menu.Item key="/style-transfer">Style Transfer</Menu.Item>
          </Link>
        </Menu>
      </Header>
      <Content className={styles.content}>
        <div className={styles.siteLayoutContent}>{children}</div>
      </Content>
      <Footer style={{ textAlign: "center" }}>
        DLSINC 2021 Created by R&D
      </Footer>
    </Layout>
  );
};

export default MainLayout;

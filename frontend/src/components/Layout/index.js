import { Layout, Menu, Breadcrumb } from "antd";
import styles from "./Layout.module.scss";
import logoImg from "assets/images/logo-white.svg";
import { Link, useLocation } from "react-router-dom";

const { Header, Content, Footer } = Layout;

const links = [
  {
    to: "/",
    title: "Remove Background",
  },
  {
    to: "/portrait-sketch",
    title: "Portrait Sketch",
  },
  {
    to: "/style-transfer",
    title: "Style Transfer",
  },
];

const MainLayout = ({ children }) => {
  const location = useLocation();
  console.log(location)
  return (
    <Layout className={styles.layout}>
      <Header>
        <div className={styles.logo}>
          <img src={logoImg} alt="Logo" />
        </div>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={[location.pathname]}>
          {links.map((link) => (
            <Menu.Item key={link.to}>
              <Link to={link.to}>{link.title}</Link>
            </Menu.Item>
          ))}
        </Menu>
      </Header>
      <Content className={styles.content}>
        <div className={styles.siteLayoutContent}>{children}</div>
      </Content>
      <Footer style={{ textAlign: "center" }}>
        DLSINC 2021 Created by R&D Team
      </Footer>
    </Layout>
  );
};

export default MainLayout;

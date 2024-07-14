import React from "react";
import styles from './Header.module.css'

const Header = () => {
  return (
    <div className={styles.header}>
      <h1>My blog</h1>
      <p>Blog powered with FastAPI and React</p>
    </div>
  );
};

export default Header;

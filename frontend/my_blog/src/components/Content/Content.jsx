import React from "react";
import Articles from "./Articles/Articles.jsx";
import Tags from "./Tags/Tags.jsx";
import styles from './Content.module.css'

const Content = () => {
  return (
    <div className={styles.content}>
      <Articles />
      <Tags />
    </div>
  );
};

export default Content;

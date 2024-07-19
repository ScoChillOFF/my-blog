import React from "react";
import Articles from "./Articles/Articles.jsx";
import CreateArticleForm from "./Articles/CreateArticleForm/CreateArticleForm.jsx";
import Tags from "./FilterSection/FilterSection.jsx";
import styles from "./Content.module.css";

const Content = () => {
  return (
    <div className={styles.content}>
      <div className={styles.leftWrapper}>
        <Articles />
      </div>
      <Tags />
    </div>
  );
};

export default Content;

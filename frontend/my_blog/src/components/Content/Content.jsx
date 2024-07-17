import React from "react";
import Articles from "./Articles/Articles.jsx";
import CreateArticleForm from "./CreateArticleForm/CreateArticleForm.jsx";
import Tags from "./FilterSection/FilterSection.jsx";
import styles from "./Content.module.css";

const Content = () => {
  return (
    <div className={styles.content}>
      <div className={styles.leftWrapper}>
        <CreateArticleForm />
        <div className={styles.divider}></div>
        <Articles />
      </div>
      <Tags />
    </div>
  );
};

export default Content;

import React from "react";
import styles from "./Article.module.css";

function formatDate(strDateTime) {
  const date = new Date(strDateTime);

  const dateOptions = {
    day: "2-digit",
    month: "short",
    year: "numeric",
  };

  const timeOptions = {
    hour: "2-digit",
    minute: "2-digit",
  };

  const time = date.toLocaleTimeString("en-US", timeOptions);

  const formattedDate = date.toLocaleDateString("en-US", dateOptions);

  return `${time} ${formattedDate}`;
}

const Article = ({ article }) => {
  return (
    <div className={styles.article}>
      <h3>{article.title}</h3>
      <p>{article.content}</p>
      <div>
        <span></span>
        <span>{formatDate(article.created_at)}</span>
      </div>
    </div>
  );
};

export default Article;

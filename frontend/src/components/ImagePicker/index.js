import { Col, Row } from "antd";
import React from "react";
import styles from "./ImagePicker.module.scss";
import cn from "classnames";

const ImagePicker = ({ images, value = "", onChange = () => {} }) => {
  return (
    <Row>
      {images.map((image) => (
        <Col md={6} key={image.id} className={styles.col}>
          <div
            style={{
              width: "100%",
              height: "100%",
              padding: 8,
              position: "absolute",
              top: 0,
            }}
          >
            <div
              className={cn(
                styles.imageWrapper,
                value === image.id && styles.actived
              )}
              onClick={() => onChange(image.id)}
            >
              <img src={image.src} />
            </div>
          </div>
        </Col>
      ))}
    </Row>
  );
};

export default ImagePicker;

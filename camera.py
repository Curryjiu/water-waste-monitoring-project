import cv2
import time
import os


def main(camera_index, window_name="Camera Preview"):
    """
    打开视频采集设备并显示实时画面

    参数:
        camera_index: 视频设备索引，默认0
        window_name: 显示窗口名称
    """
    # 创建保存截图的目录
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # 打开视频捕获设备
    cap = cv2.VideoCapture(camera_index)

    # 检查设备是否成功打开
    if not cap.isOpened():
        print(f"无法打开设备 {camera_index}")
        return

    # 获取视频的宽度、高度和帧率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"视频设备参数: 宽度={width}, 高度={height}, 帧率={fps}")

    # 创建窗口
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # 记录截图序号
    screenshot_count = 0

    print("提示:")
    print("  - 按 's' 键保存当前画面为截图")
    print("  - 按 'q' 键退出程序")

    while True:
        # 读取一帧
        ret, frame = cap.read()

        # 检查是否成功读取帧
        if not ret:
            print("无法获取帧，退出...")
            break

        # 显示帧
        cv2.imshow(window_name, frame)

        # 处理键盘输入
        key = cv2.waitKey(1) & 0xFF

        # 按 's' 键保存截图
        if key == ord('s'):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_file = f"screenshots/screenshot_{timestamp}_{screenshot_count}.png"
            cv2.imwrite(screenshot_file, frame)
            print(f"已保存截图: {screenshot_file}")
            screenshot_count += 1

        # 按 'q' 键退出
        elif key == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 如果有多个摄像头，可以尝试不同的索引值(0,1,2...)
    main(camera_index=1)
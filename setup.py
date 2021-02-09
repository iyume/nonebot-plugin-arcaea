from setuptools import setup


def get_dis():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


def main():
    dis = get_dis()
    setup(
        name="nonebot-plugin-arcaea",
        version="0.1.3",
        url="https://github.com/iyume/nonebot-plugin-arcaea",
        keywords=["nonebot"],
        description="An arcaea rhythm game score-querying plugin for nonebot2",
        long_description_content_type="text/markdown",
        long_description=dis,
        author="iyume",
        author_email="iyumelive@gmail.com",
        python_requires=">=3.8",
        packages=['nonebot_plugin_arcaea'],
        install_requires=["databases", "aiosqlite", "pillow", "httpx", "brotli"],
        license='GPLv3',
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
        include_package_data=True,
    )


if __name__ == '__main__':
    main()

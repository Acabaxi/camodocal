#ifndef CIRCLEGRID_H
#define CIRCLEGRID_H

#include <boost/shared_ptr.hpp>
#include <opencv2/core/core.hpp>

namespace camodocal
{

// forward declarations
class CircleGridCorner;
typedef boost::shared_ptr<CircleGridCorner> CircleGridCornerPtr;
class CircleGridQuad;
typedef boost::shared_ptr<CircleGridQuad> CircleGridQuadPtr;

class CircleGrid
{
public:
    CircleGrid(cv::Size boardSize, cv::Mat& image);

    void findCorners(bool useOpenCV = false);
    const std::vector<cv::Point2f>& getCorners(void) const;
    bool cornersFound(void) const;

    const cv::Mat& getImage(void) const;
    const cv::Mat& getSketch(void) const;

private:
    bool findCircleGridCorners(const cv::Mat& image,
                               const cv::Size& patternSize,
                               std::vector<cv::Point2f>& corners,
                               int flags, bool useOpenCV);


    cv::Mat mImage;
    cv::Mat mSketch;
    std::vector<cv::Point2f> mCorners;
    cv::Size mBoardSize;
    bool mCornersFound;
};

}

#endif

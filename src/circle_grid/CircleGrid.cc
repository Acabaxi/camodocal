#include "camodocal/circle_grid/CircleGrid.h"

#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
namespace camodocal
{

CircleGrid::CircleGrid(cv::Size boardSize, cv::Mat& image)
 : mBoardSize(boardSize)
 , mCornersFound(false)
{
    if (image.channels() == 1)
    {
        cv::cvtColor(image, mSketch, CV_GRAY2BGR);
        image.copyTo(mImage);
    }
    else
    {
        image.copyTo(mSketch);
        cv::cvtColor(image, mImage, CV_BGR2GRAY);
    }
}

void
CircleGrid::findCorners(bool useOpenCV)
{
    mCornersFound = findCircleGridCorners(mImage, mBoardSize, mCorners,
                                          CV_CALIB_CB_ADAPTIVE_THRESH +
                                          CV_CALIB_CB_NORMALIZE_IMAGE +
                                          CV_CALIB_CB_FILTER_QUADS +
                                          CV_CALIB_CB_FAST_CHECK,
                                          useOpenCV);

    if (mCornersFound)
    {
        // draw CircleGrid corners
        cv::drawChessboardCorners(mSketch, mBoardSize, mCorners, mCornersFound);
    }
}

const std::vector<cv::Point2f>&
CircleGrid::getCorners(void) const
{
    return mCorners;
}

bool
CircleGrid::cornersFound(void) const
{
    return mCornersFound;
}

const cv::Mat&
CircleGrid::getImage(void) const
{
    return mImage;
}

const cv::Mat&
CircleGrid::getSketch(void) const
{
    return mSketch;
}

bool
CircleGrid::findCircleGridCorners(const cv::Mat& image,
                                  const cv::Size& patternSize,
                                  std::vector<cv::Point2f>& corners,
                                  int flags, bool useOpenCV)
{
    std::cout << "here " << std::endl;
    if (useOpenCV)
    {
	    // Avoid filtering pattern when it's too close to the camera
	    cv::SimpleBlobDetector::Params params;
	    params.maxArea = 10000;
	    params.minArea = 100;
	    cv::Ptr<cv::FeatureDetector> blobDetector = cv::SimpleBlobDetector::create(params);

        bool zas = cv::findCirclesGrid(image, patternSize, corners,
		                            cv::CALIB_CB_ASYMMETRIC_GRID | cv::CALIB_CB_CLUSTERING, blobDetector);
        return zas;
    }
    return false;
}

}

import sys, os
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

def create_many_blobs(number_of_blobs, height, fluctuate_ratio=0.5, num_of_points=10, interp_kind='cubic'):
    frames = np.zeros((number_of_blobs, height, height), dtype=int)
    for i in range(number_of_blobs):
        frames[i, :, :] = create_blob(height, fluctuate_ratio, num_of_points, interp_kind)
    return frames


def create_blob(height, fluctuate_ratio=0.5, num_of_points=10, interp_kind='cubic'):
    frame = np.ones((height, height)) * 255  # Default white background
    center = height // 2  # The center of the frame
    # Maximum radius that will fit the frame
    max_radius = center
    fluc_range = max_radius * fluctuate_ratio  # How much will the blob fluctuate

    random_radius = np.random.randint(
        max_radius - fluc_range, max_radius, num_of_points)
    # Pick random points in the range of fluctuation

    random_radius = np.concatenate((random_radius, [random_radius[0]]))
    # For the loop to be closed add the first value to the last
    thetas = np.arange(-np.pi, np.pi, 2 * np.pi / num_of_points)
    # Interval of each random point on the angle domain
    thetas = np.concatenate((thetas, [np.pi]))
    # Two pi will be equal to 0 as we added the first element also to the last in random_radius
    # so the loop will be closed.
    boundry_function = interp1d(thetas, random_radius, kind=interp_kind)
    # Create interpolation function

    x_matrix = np.zeros((height, height))
    # This matrix holds the x indices of the frame, every row is the same
    x_matrix[:, np.arange(0, height)] = np.arange(
        0 - center, height - center)
    # Here is the assignment for every row
    y_matrix = np.copy(x_matrix)
    y_matrix = y_matrix.T  # y matrix is just the transpose of the x matrix

    theta_matrix = np.arctan2(y_matrix, x_matrix)
    radius_matrix = np.sqrt((np.square(x_matrix) + np.square(y_matrix)))

    # These two matrices are angle and radius information of each point on the
    # frame

    rad_val_matrix = boundry_function(theta_matrix)
    # This returns the boundry function's radius information for each angle on the frame
    # This is actually a vectorization trick becasue in the frame the lines having the same
    # angle will have the same radius value

    frame = (rad_val_matrix > radius_matrix).astype(int)
    # This is where we decide if the point on the frame is inside or outside
    # of the boundry function

    # plt.imshow(frame, cmap='gray')  # These are to see the blobs
    # plt.show()

    return frame
"""
    Parameters:
        height: Height and width of the square frame
        fluctuate_ratio: This is the ratio to determine the fraction of the maximum radius to oscillate
                         For example if max radius is 100 and ratio is 0.1 then the blob will be the
                         oscillation of a circle in the range 100 * 0.1 = 10 -> 90 - 100
                                                           if 150 * 0.3 = 45 -> 105 - 150
                         In other words how much will the radius shrink to make the oscillation.
                         If this parameter is bigger than the oscillation amplitude is bigger.
        num_of_points: This is the number of points to randomly pick then interpolate, if this is
                       high then the frequency will be higher.
        interp_kind: The kind of the interpolation, default is cubic but any polynomial degree can
                     be given as an integer.

    Returns:
        frame: The blob mask as an integer NumPy array.
"""

def main():
    try:
        size = int(sys.argv[1]) # The height and width of the blob, affects resolution
        fluc_rate = float(sys.argv[2])
        num_points = int(sys.argv[3])
        if(len(sys.argv) == 5):
            number_of_blobs = int(sys.argv[4])
        else:
            number_of_blobs = 1
    except:
        print("Invalid arguments. Please enter as [size, fluctuation rate, number of points]")
        raise

    if not os.path.exists("./blobs"):
        os.makedirs("./blobs")

    
    frames = create_many_blobs(number_of_blobs, size, fluc_rate, num_points)
    for i in range(frames.shape[0]):
        plt.imsave("./blobs/blob" + str(i+1) + ".png", frames[i, :, :], cmap="gray")
        plt.show()



if __name__ == "__main__":
    main()

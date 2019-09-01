import numpy as np
import pandas as pd
import re

def sorted_signatures(signature_list):
    """
    this function takes in a list of signatures and returns a data frame of the results

    Keyword arguments:
    signature_list -- a list of strings to be cleaned for hair products
    """
    # sort the signatures up the signatures
    # Take the four characteristics and put them in lists (put absent ones as null values) while removing them
    # remove www, http, cg, cgm completly
    # put the remainder into a string of no puntation and lowercase(inspect these and maybe apply stop words...maybe)
    # Finally read the string

    curls = []
    density = []
    porosity = []
    texture = []
    products = []

    # maybe make a seperate clean up function fromthe make a data frame function with all of this substitutions and different product names
    for s in signature_list:
        s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
        s = s.lower()
        s = re.sub(r"\n", " ", s)
        s = re.sub(r"med\s", "medium ", s)
        s = re.sub(r"hi\s", "high ", s)
        s = re.sub(r"po\s", "porosity ", s)
        s = re.sub(r"den\s", "density ", s)
        # lot of hair --> thick density

        ##################
        ### Curl shape
        curl_pattern = r"\da|\db|\dc"
        curl_result1 = re.search(curl_pattern, s)

        #First
        try:
            s = s.replace(curl_result1.group(), "")
            curls.append(curl_result1.group())
        except AttributeError:
            #if error put np.nan into list
            curls.append(np.nan)

        curl_result2 = re.search(curl_pattern, s)
        try:
            s = s.replace(curl_result2.group(), "")
            curls.append(curl_result2.group())
            two_shapes = True
        except AttributeError:
            #if error put np.nan into list for first instance and set a variable for other characteristics to know if they need to put two row
            two_shapes = False

        s = re.sub("  ", " ",s)
        s = re.sub("   ", " ",s)

        ##################
        ### Texture Patten
        # Check all the conditions that might be present to describe the texture including if they don't follow it with the word texture
        texture_pattern1 = r"texture"
        texture_result1 = re.search(texture_pattern1, s)

        texture_pattern2 = r"course"
        course_result = re.search(texture_pattern2, s)

        texture_pattern3 = r"fine"
        fine_result = re.search(texture_pattern3, s)

        texture_pattern4 = r"\w*(?= texture)"
        texture_result4 = re.search(texture_pattern4, s)

        if texture_result1 is not None:
            try:
                s = s.replace(texture_result4.group(), texture_result4.group())
                s = re.sub(r"\w*( texture)", "", s)
                if two_shapes:
                    texture.append(texture_result4.group())
                    texture.append(texture_result4.group())
                else:
                    texture.append(texture_result4.group())
            except AttributeError:
                if two_shapes:
                    texture.append(np.nan)
                    texture.append(np.nan)
                else:
                    texture.append(np.nan)

        elif course_result is not None:
            s = s.replace(course_result.group(), "")
            if two_shapes:
                texture.append(course_result.group())
                texture.append(course_result.group())
            else:
                texture.append(course_result.group())

        elif fine_result is not None:
            s = s.replace(fine_result.group(), "")
            if two_shapes:
                texture.append(fine_result.group())
                texture.append(fine_result.group())
            else:
                texture.append(fine_result.group())
        else:
            if two_shapes:
                texture.append(np.nan)
                texture.append(np.nan)
            else:
                texture.append(np.nan)

        s = re.sub("  ", " ",s)
        s = re.sub("   ", " ",s)

        ##################
        ### Porosity Pattern
        porosity_pattern = r"\w*(?= porosity)"
        porosity_result = re.search(porosity_pattern, s)

        try:
            s = s.replace(porosity_result.group(), porosity_result.group())
            s = re.sub(r"\w*( porosity)", "", s)
            if two_shapes:
                porosity.append(porosity_result.group())
                porosity.append(porosity_result.group())
            else:
                porosity.append(porosity_result.group())
        except AttributeError:
            if two_shapes:
                porosity.append(np.nan)
                porosity.append(np.nan)
            else:
                porosity.append(np.nan)

        s = re.sub("  ", " ",s)
        s = re.sub("   ", " ",s)

        ##################
        ### Density Pattern
        density_pattern1 = r"density"
        density_result1 = re.search(density_pattern1, s)

        density_pattern2 = r"thin"
        thin_result = re.search(density_pattern2, s)

        density_pattern3 = r"thick"
        thick_result = re.search(density_pattern3, s)

        density_pattern4 = r"\w*(?= density)"
        density_result4 = re.search(density_pattern4, s)

        if density_result1 is not None:
            try:
                s = s.replace(density_result4.group(), density_result4.group())
                s = re.sub(r"\w*( density)", "", s)
                if two_shapes:
                    density.append(density_result4.group())
                    density.append(density_result4.group())
                else:
                    density.append(density_result4.group())
            except AttributeError:
                if two_shapes:
                    density.append(np.nan)
                    density.append(np.nan)
                else:
                    density.append(np.nan)

        elif thin_result is not None:
            s = s.replace(thin_result.group(), "")
            if two_shapes:
                density.append(thin_result.group())
                density.append(thin_result.group())
            else:
                density.append(thin_result.group())

        elif thick_result is not None:
            s = s.replace(thick_result.group(), "")
            if two_shapes:
                density.append(thick_result.group())
                density.append(thick_result.group())
            else:
                density.append(thick_result.group())

        else:
            if two_shapes:
                density.append(np.nan)
                density.append(np.nan)
            else:
                density.append(np.nan)



        #### Maybe go back now and remove third curl pattern references, medium, fine, thick, thin,corse etc since it must have ben two parters
        #s = s.replace()
        s = re.sub(r"(http.*?\s)", "", s)
        s = re.sub(r"(www.*?\s)", "", s)
        s = re.sub(r"(cg.*?\s)", "", s)
        s = re.sub(r"\s\da|\s\db|\s\dc", "", s)
        s = re.sub("fine", "", s)
        s = re.sub("course", "", s)
        s = re.sub("thick", "", s)
        s = re.sub("thin", "", s)
        s = re.sub("medium", "", s)
        s = re.sub("  ", " ",s)
        s = re.sub("   ", " ",s)

        if two_shapes:
            products.append(s)
            products.append(s)
        else:
            products.append(s)

        # check if all are the same length
    if len(curls) == len(density) == len(porosity) == len(texture) == len(products):
        None
    else:
        print('differeing list lengths')

    # Put the resulting lists into a dictionary for then making a dataframe
    characteristics_dict = {'curl_pattern': curls, 'density': density, 'porosity': porosity, 'texture': texture, 'products': products}

    signature_df = pd.DataFrame(characteristics_dict)

    return signature_df


############################################

def cleaned_signatures(sorted_signature_df):
    """
    This function takes in a dataframe of already sorted signatures and outputs those signatures cleaned to return only the allowed values for each characteristic and no blank products

    Keyword arguments:
    sorted_signature_df -- a df of sorted signatures to be cleaned. needs columns named: curl_product, texture, density, porosity, and product. The index is unimportant. Everything should be a string.
    """
    # Drop all rows that were null in all characteristics
    all_nan_dropped_df = sorted_signature_df.dropna(axis=0, how='all', subset=['curl_pattern', 'density', 'porosity', 'texture'], inplace=False)

    # sort the curl_pattern column to only contain the correct values and NaN

    ##################
    ### Curl shape
    # Sort out values that are not the allowed values
    all_nan_dropped_df.loc[(all_nan_dropped_df.curl_pattern != '2a') &
        (all_nan_dropped_df.curl_pattern  != '2b') & (all_nan_dropped_df.curl_pattern != '2c') &
        (all_nan_dropped_df.curl_pattern != '3a') & (all_nan_dropped_df.curl_pattern != '3b') & (all_nan_dropped_df.curl_pattern != '3c') & (all_nan_dropped_df.curl_pattern != '4a') & (all_nan_dropped_df.curl_pattern != '4b') & (all_nan_dropped_df.curl_pattern != '4c') &
        (all_nan_dropped_df.curl_pattern != '1c'), 'curl_pattern'] = np.nan


    ##################
    ### Porosity Pattern
    # take common words used to decribe the porosity and sort them into one of the three catagories
    all_nan_dropped_df.loc[all_nan_dropped_df.porosity == 'medium', 'porosity'] = 'normal'
    all_nan_dropped_df.loc[all_nan_dropped_df.porosity == 'average', 'porosity'] = 'normal'

    # Sort out values that are not the allowed values
    all_nan_dropped_df.loc[(all_nan_dropped_df.porosity != 'normal') &
        (all_nan_dropped_df.porosity != 'high') & (all_nan_dropped_df.porosity != 'low'), 'porosity'] = np.nan


    ##################
    ### Density Pattern
    # take common words used to decribe the density and sort them into one of the three catagories
    all_nan_dropped_df.loc[all_nan_dropped_df.density == 'normal', 'density'] = 'medium'
    all_nan_dropped_df.loc[all_nan_dropped_df.density == 'high', 'density'] = 'thick'
    all_nan_dropped_df.loc[all_nan_dropped_df.density == 'low', 'density'] = 'thin'

    # Sort out values that are not the allowed values
    all_nan_dropped_df.loc[(all_nan_dropped_df.density != 'medium') &
        (all_nan_dropped_df.density != 'thin') & (all_nan_dropped_df.density != 'thick'), 'density'] = np.nan


    ##################
    ### Texture Patten
    # take common words used to decribe the texture and sort them into one of the three catagories
    all_nan_dropped_df.loc[all_nan_dropped_df.texture == 'normal', 'texture'] = 'medium'
    all_nan_dropped_df.loc[all_nan_dropped_df.texture == 'course', 'texture'] = 'coarse'

    # Sort out values that are not the allowed values
    all_nan_dropped_df.loc[(all_nan_dropped_df.texture != 'medium') &
        (all_nan_dropped_df.texture != 'fine') & (all_nan_dropped_df.texture != 'coarse'), 'texture'] = np.nan
